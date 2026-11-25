from flask import Flask, render_template, jsonify, request
import subprocess
import os
import psutil
import json
from datetime import datetime
from influxdb_client import InfluxDBClient
import threading

app = Flask(__name__)

# InfluxDB configuration
INFLUXDB_URL =  "http://influxdb:8086"
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = "fisens"
INFLUXDB_BUCKET = "sensors"

# Logger process
logger_process = None
logger_lock = threading.Lock()

def get_influxdb_client():
    """Get InfluxDB client"""
    try:
        client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        return client
    except Exception as e:
        print(f"Error connecting to InfluxDB: {e}")
        return None

def get_latest_peaks():
    """Get latest peak data from InfluxDB"""
    try:
        client = get_influxdb_client()
        if not client:
            return None

        query = f'''
        from(bucket:"{INFLUXDB_BUCKET}")
          |> range(start: -1h)
          |> filter(fn: (r) => r._measurement == "peak_spectrum")
          |> sort(columns: ["_time"], desc: true)
          |> limit(n: 10)
        '''

        query_api = client.query_api()
        result = query_api.query(query=query)

        peaks_data = {}
        for table in result:
            for record in table.records:
                try:
                    tags = record.values.get('tags', {}) if hasattr(record, 'values') else {}
                    if isinstance(tags, dict):
                        peak_num = tags.get('peak_number', '1')
                    else:
                        peak_num = '1'

                    field = record.values.get('_field', '')

                    if peak_num not in peaks_data:
                        peaks_data[peak_num] = {
                            'peak_number': peak_num,
                            'wavelength_nm': 0.0,
                            'amplitude': 0.0,
                            'timestamp': str(record.values.get('_time', '')) if hasattr(record, 'values') else ''
                        }

                    value = record.values.get('_value') if hasattr(record, 'values') else None

                    if field == 'peak_wavelength_nm':
                        peaks_data[peak_num]['wavelength_nm'] = float(value) if value else 0.0
                    elif field == 'peak_amplitude':
                        peaks_data[peak_num]['amplitude'] = float(value) if value else 0.0
                except Exception as record_error:
                    print(f"Error processing record: {record_error}")
                    continue

        return sorted(peaks_data.values(), key=lambda x: int(x['peak_number'])) if peaks_data else []

    except Exception as e:
        print(f"Error fetching peaks: {e}")
        return []

def start_logger():
    """Start the fisens logger process"""
    global logger_process

    with logger_lock:
        if logger_process and logger_process.poll() is None:
            return {"status": "already_running", "message": "Logger is already running"}

        try:
            project_dir = os.path.dirname(os.path.abspath(__file__))

            logger_process = subprocess.Popen(
                ["python", "log_fisens_multipass.py"],
                cwd=project_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            return {"status": "started", "message": "Logger started successfully", "pid": logger_process.pid}

        except Exception as e:
            return {"status": "error", "message": f"Failed to start logger: {str(e)}"}

def stop_logger():
    """Stop the fisens logger process"""
    global logger_process

    with logger_lock:
        if not logger_process or logger_process.poll() is not None:
            return {"status": "not_running", "message": "Logger is not running"}

        try:
            logger_process.terminate()
            logger_process.wait(timeout=5)
            logger_process = None
            return {"status": "stopped", "message": "Logger stopped successfully"}

        except subprocess.TimeoutExpired:
            logger_process.kill()
            logger_process = None
            return {"status": "stopped", "message": "Logger killed (did not terminate gracefully)"}

        except Exception as e:
            return {"status": "error", "message": f"Failed to stop logger: {str(e)}"}

def is_logger_running():
    """Check if logger is running"""
    global logger_process

    if logger_process is None:
        return False

    return logger_process.poll() is None

@app.route('/')
def index():
    """Serve the dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get logger status"""
    running = is_logger_running()
    peaks = get_latest_peaks()

    return jsonify({
        'logger_running': running,
        'peaks': peaks,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/start', methods=['POST'])
def api_start():
    """Start the logger"""
    result = start_logger()
    return jsonify(result)

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """Stop the logger"""
    result = stop_logger()
    return jsonify(result)

@app.route('/api/peaks')
def api_peaks():
    """Get latest peaks"""
    peaks = get_latest_peaks()
    return jsonify({
        'peaks': peaks,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
