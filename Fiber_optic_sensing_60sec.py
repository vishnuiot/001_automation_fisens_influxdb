import time
import serial
import os
import numpy as np
from datetime import datetime, timezone, timedelta
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# InfluxDB Configuration
client = InfluxDBClient(
    url="http://localhost:8086",
    token=os.getenv("INFLUXDB_TOKEN"),
    org="fisens"
)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Sensor Configuration
SERIAL_PORT = "COM4"
BAUD_RATE = 3000000
RECONNECT_DELAY = 5
LOG_INTERVAL = 5

# Run Duration (in seconds). The batch file runs this script once and then exits.
RUN_DURATION = 120

# LabVIEW Settings
INTEGRATION_TIME_MS = 100
RAW_RATE_HZ = 9

# Wavelength Calibration
FBG_MIN_NM = 800.0
FBG_MAX_NM = 900.0
SPECTRUM_POINTS = 1492

# Peak Detection Configuration
MIN_AMPLITUDE_TO_LOG = 2000
MIN_AMPLITUDE_SECONDARY_PEAKS = 3200
MAX_PEAKS_TO_LOG = 3

# GLOBAL
WAVELENGTH_CALIBRATION = None


def spectrum_index_to_wavelength(spectrum_index):
    """Convert spectrum index to wavelength in nm using actual calibration"""
    global WAVELENGTH_CALIBRATION

    if WAVELENGTH_CALIBRATION and spectrum_index < len(WAVELENGTH_CALIBRATION):
        wl_raw = WAVELENGTH_CALIBRATION[spectrum_index]
        if wl_raw > 0:
            return wl_raw / 10000.0

    # Fallback: linear interpolation
    return FBG_MIN_NM + (spectrum_index / SPECTRUM_POINTS) * (FBG_MAX_NM - FBG_MIN_NM)


def read_spectrum(ser):
    """Read spectrum from sensor (1492 points)"""
    try:
        # Clear any pending data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        time.sleep(0.2)

        # Send spectrum command with proper format
        ser.write(b"s>")
        time.sleep(0.5)

        # Read in chunks to ensure we get all data
        data = b""
        timeout_count = 0
        while len(data) < 2994 and timeout_count < 3:
            chunk = ser.read(2994 - len(data))
            if chunk:
                data += chunk
                timeout_count = 0
            else:
                timeout_count += 1
                time.sleep(0.05)

        if not data or len(data) < 100:
            raise Exception(f"Invalid spectrum data (got {len(data)} bytes)")

        spectrum_bytes = np.frombuffer(data[:-4], dtype=np.uint16)
        spectrum_list = list(spectrum_bytes[3:])
        return spectrum_list
    except Exception as e:
        print(f"⚠️ Spectrum read error: {e}")
        return None


def read_wavelength(ser):
    """Read wavelength calibration (int32 array, trimmed to spectrum size)"""
    global WAVELENGTH_CALIBRATION
    try:
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        time.sleep(0.1)

        ser.write(b"WLL>")
        time.sleep(0.2)

        # Read in chunks to ensure we get all data
        data = b""
        timeout_count = 0
        while len(data) < 8000 and timeout_count < 3:
            chunk = ser.read(1024)
            if chunk:
                data += chunk
                timeout_count = 0
            else:
                timeout_count += 1
                time.sleep(0.05)

        if not data or len(data) < 100:
            raise Exception(f"Invalid wavelength data (got {len(data)} bytes)")

        # WLL returns int32 values
        wavelength_bytes = np.frombuffer(data[:-4], dtype=np.int32)
        wavelength_list = list(wavelength_bytes)

        # CRITICAL: Trim to SPECTRUM_POINTS (1492)
        original_len = len(wavelength_list)
        if len(wavelength_list) > SPECTRUM_POINTS:
            wavelength_list = wavelength_list[:SPECTRUM_POINTS]
            print(f"  [WLL] Trimmed {original_len} → {SPECTRUM_POINTS} points")

        WAVELENGTH_CALIBRATION = wavelength_list
        return wavelength_list
    except Exception as e:
        print(f"⚠️ Wavelength read error: {e}")
        return None


def find_peaks(spectrum_list):
    """Find top 3 amplitude peaks with clustering. Returned strongest first."""
    if not spectrum_list:
        return []

    # Find all points above threshold
    candidates = [(idx, amp) for idx, amp in enumerate(spectrum_list)
                  if amp >= MIN_AMPLITUDE_TO_LOG]

    if not candidates:
        return []

    # Sort by amplitude to process strongest first
    candidates.sort(key=lambda x: x[1], reverse=True)

    # Cluster nearby peaks (within 20 points = 1 peak)
    distinct_peaks = []
    used_indices = set()

    for idx, amp in candidates:
        # Skip if already part of another peak cluster
        if any(abs(idx - used_idx) < 20 for used_idx in used_indices):
            continue

        # This is a new distinct peak
        distinct_peaks.append((idx, amp))
        used_indices.add(idx)

        if len(distinct_peaks) >= 3:
            break

    return distinct_peaks


def apply_secondary_threshold(peaks):
    """Keep the strongest peak unconditionally; secondary peaks must reach
    MIN_AMPLITUDE_SECONDARY_PEAKS to be logged. Input is strongest first."""
    if not peaks:
        return []
    strongest = peaks[0]
    secondary = [p for p in peaks[1:] if p[1] >= MIN_AMPLITUDE_SECONDARY_PEAKS]
    return [strongest] + secondary


def log_to_influxdb(peaks, timestamp):
    """Log peaks to InfluxDB sorted by wavelength (lowest to highest)"""
    try:
        # Convert peaks to list with wavelengths and sort by wavelength
        peaks_with_wavelengths = []
        for peak_idx, peak_amp in peaks:
            wavelength_nm = spectrum_index_to_wavelength(peak_idx)
            peaks_with_wavelengths.append({
                'wavelength_nm': wavelength_nm,
                'peak_amp': peak_amp,
                'peak_idx': peak_idx
            })

        # Sort by wavelength (lowest to highest)
        peaks_with_wavelengths.sort(key=lambda x: x['wavelength_nm'])

        # Log exactly 3 peaks sorted by wavelength
        for peak_position in range(1, 4):
            if peak_position <= len(peaks_with_wavelengths):
                peak_data = peaks_with_wavelengths[peak_position - 1]
                wavelength_nm = peak_data['wavelength_nm']
                peak_amp = peak_data['peak_amp']
                peak_idx = peak_data['peak_idx']

                # Identify by wavelength range
                if wavelength_nm >= 804 and wavelength_nm < 810:
                    grating_name = "P1 - Blue (806 nm)"
                elif wavelength_nm >= 810 and wavelength_nm < 815:
                    grating_name = "P2 - Green (813 nm)"
                elif wavelength_nm >= 815 and wavelength_nm <= 820:
                    grating_name = "P3 - Red (816 nm)"
                else:
                    grating_name = f"P{peak_position} - Unknown"
            else:
                # Missing peak - log as zero
                wavelength_nm = 0.0
                peak_amp = 0
                peak_idx = 0
                grating_name = f"P{peak_position} - Missing"

            point = Point("peak_spectrum") \
                .tag("source", "fisens_sensor") \
                .tag("port", SERIAL_PORT) \
                .tag("peak_number", str(peak_position)) \
                .tag("grating_name", grating_name) \
                .field("peak_wavelength_nm", float(wavelength_nm)) \
                .field("peak_amplitude", float(peak_amp)) \
                .field("peak_index", int(peak_idx)) \
                .time(timestamp)

            write_api.write(bucket="sensors", org="fisens", record=point)

        return True
    except Exception as e:
        print(f"❌ InfluxDB Error: {e}")
        return False


def plot_spectrum(spectrum_list, peaks, timestamp):
    """Plot spectrum with detected peaks and save with datetime"""
    try:
        if not WAVELENGTH_CALIBRATION:
            return

        # Create measurement_plots folder if it doesn't exist
        if not os.path.exists('measurement_plots'):
            os.makedirs('measurement_plots')

        # Convert calibration to wavelength
        wavelengths = np.array([x / 10000.0 for x in WAVELENGTH_CALIBRATION])

        plt.figure(figsize=(14, 5))
        plt.plot(wavelengths, spectrum_list, 'b-', linewidth=0.8, label='Spectrum')

        # Plot detected peaks
        colors = ['red', 'green', 'blue']
        for i, (peak_idx, peak_amp) in enumerate(peaks):
            peak_wl = spectrum_index_to_wavelength(peak_idx)
            plt.axvline(peak_wl, color=colors[i], linestyle='--', linewidth=2,
                        label=f'Peak {i+1}: {peak_wl:.2f}nm @ {peak_amp}')

        plt.xlabel('Wavelength (nm)', fontsize=12)
        plt.ylabel('Amplitude', fontsize=12)
        plt.title('Fisens FBG Spectrum - Real-time Detection', fontsize=14)
        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Generate filename with datetime
        timestamp_str = timestamp.astimezone().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'measurement_plots/spectrum_{timestamp_str}.png'
        plt.savefig(filename, dpi=100)
        plt.close()
        print(f"  📊 Spectrum plot saved: {filename}")
    except Exception as e:
        print(f"⚠️ Plot error: {e}")


def reset_serial_port(ser):
    """Reset serial port without restarting the computer"""
    try:
        if ser:
            try:
                if ser.is_open:
                    ser.close()
                    print("  Serial port closed")
                    time.sleep(2)
            except:
                pass

        # Reopen the port
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            parity=serial.PARITY_NONE,
            bytesize=8,
            timeout=5,
            stopbits=serial.STOPBITS_ONE
        )
        time.sleep(3)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        time.sleep(1)
        print("  ✅ Serial port reset successfully")
        return ser
    except Exception as e:
        print(f"  ❌ Serial reset failed: {e}")
        return None


def connect_to_sensor():
    """Connect to FBG sensor via serial with exponential backoff"""
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            ser = serial.Serial(
                port=SERIAL_PORT,
                baudrate=BAUD_RATE,
                parity=serial.PARITY_NONE,
                bytesize=8,
                timeout=5,
                stopbits=serial.STOPBITS_ONE
            )
            time.sleep(3)
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            time.sleep(1)
            return ser
        except serial.SerialException as e:
            if attempt < max_attempts:
                wait_time = 2 ** attempt
                print(f"  ⚠️ Attempt {attempt}/{max_attempts} failed: {e}")
                print(f"  ⏳ Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"❌ Serial Connection Failed after {max_attempts} attempts: {e}")
                print(f"  💡 Try: python clear_com_port.py")
                return None
    return None


def get_device_info(ser):
    """Get device model from sensor"""
    try:
        ser.write(b"?>")
        device_model = ser.read(20).decode().strip()
        return device_model
    except:
        return "Unknown Device"


# Main Logger
if __name__ == "__main__":
    print(f"🔌 Fiber Optic Sensing - 60 Second Session Logger")
    print(f"📍 Port: {SERIAL_PORT} @ {BAUD_RATE} baud")
    print(f"📊 InfluxDB: http://localhost:8086")
    print(f"🎯 Peaks: Top {MAX_PEAKS_TO_LOG}, Min Amplitude: {MIN_AMPLITUDE_TO_LOG}, "
          f"Secondary Min: {MIN_AMPLITUDE_SECONDARY_PEAKS}")
    print(f"⏱️  Log Interval: {LOG_INTERVAL}s")
    print(f"⏰ Run Duration: {RUN_DURATION}s (then exit)")
    print(f"📈 Spectrum Plotting: ENABLED")
    print("=" * 70)

    ser = None
    counter = 0
    connected = False
    session_start = datetime.now()

    try:
        while True:
            # CHECK TIME LIMIT FIRST (before anything else)
            elapsed = (datetime.now() - session_start).total_seconds()
            if elapsed >= RUN_DURATION:
                print(f"\n⏰ Duration limit reached ({RUN_DURATION}s)")
                print(f"   Total readings: {counter}")
                print(f"   Exiting...\n")
                break

            if not connected:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🔌 Connecting to {SERIAL_PORT}...")

                # Try soft reset first
                if ser:
                    print("  Attempting soft reset...")
                    ser = reset_serial_port(ser)

                # If soft reset fails or port never existed, try fresh connection
                if not ser or not ser.is_open:
                    ser = connect_to_sensor()

                if ser and ser.is_open:
                    connected = True
                    device_info = get_device_info(ser)
                    print(f"✅ Connected | Device: {device_info}")

                    # Read wavelength calibration once per connection
                    wl = read_wavelength(ser)
                    if wl:
                        print(f"✅ Wavelength calibration loaded: {len(wl)} points")
                        print(f"   Range: {wl[0]/10000.0:.2f} - {wl[-1]/10000.0:.2f} nm\n")

                    print(f"📊 Logging to InfluxDB...\n")
                else:
                    print(f"⏳ Retry in {RECONNECT_DELAY}s...")
                    time.sleep(RECONNECT_DELAY)
                    continue

            if connected:
                counter += 1
                try:
                    print(f"[{counter}] [{datetime.now().strftime('%H:%M:%S')}] Reading...", end=" ", flush=True)

                    # Reuse the calibration from connection; re-read only if it is missing
                    wavelength = WAVELENGTH_CALIBRATION or read_wavelength(ser)
                    time.sleep(0.5)
                    spectrum = read_spectrum(ser)

                    if spectrum is None or wavelength is None:
                        print("❌ Read failed")
                        connected = False
                        ser.close()
                        time.sleep(2)
                        continue

                    peaks = apply_secondary_threshold(find_peaks(spectrum))

                    if peaks:
                        top_3 = peaks[:3]
                        print(f"Found {len(peaks)} peaks, Top 3: ", end="", flush=True)

                        for peak_num, (idx, amp) in enumerate(top_3, 1):
                            wl = spectrum_index_to_wavelength(idx)
                            print(f"P{peak_num}={wl:.2f}nm@{amp:.0f} ", end="", flush=True)

                        timestamp = datetime.now(timezone.utc)

                        # Plot spectrum with peaks
                        plot_spectrum(spectrum, peaks, timestamp)
                        if log_to_influxdb(peaks, timestamp):
                            print("✅ Logged")
                        else:
                            print("❌ Failed")
                    else:
                        print("❌ No peaks")

                    # Check time limit before sleeping
                    elapsed = (datetime.now() - session_start).total_seconds()
                    if elapsed >= RUN_DURATION:
                        print(f"\n⏰ Duration limit reached ({RUN_DURATION}s)")
                        break

                    print(f"⏳ Next: {LOG_INTERVAL}s")
                    time.sleep(LOG_INTERVAL)

                except serial.SerialException as e:
                    print(f"\n❌ Connection Lost: {e}")
                    connected = False
                    if ser:
                        try:
                            if ser.is_open:
                                ser.close()
                            time.sleep(1)
                        except:
                            pass
                    print(f"⏳ Reconnecting in {RECONNECT_DELAY}s...\n")
                    time.sleep(RECONNECT_DELAY)

                except Exception as e:
                    print(f"\n⚠️ Error: {e}")
                    time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n⛔ Stopped by user")
        if ser:
            try:
                if ser.is_open:
                    ser.close()
                    time.sleep(1)
            except:
                pass
        print("✅ Shutdown complete")

    # Always cleanup on exit
    if ser:
        try:
            if ser.is_open:
                ser.close()
        except:
            pass
    client.close()
