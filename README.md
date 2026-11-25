# FiSens InfluxDB Automation – Python Data Logging

Python scripts that read fibre optic sensor data from the FiSens / FiSpec interrogator over a serial port, save it to CSV, and write it to InfluxDB, plus the batch files used to run the software.

## Scripts

| File | Purpose |
|---|---|
| `002a_max_point_influxdb.py` | Acquire peak data and write to InfluxDB (PC) |
| `002aa_raspberrypi_max_point_influxdb copy.py` | Same logger for the Raspberry Pi |
| `001c.single_loop_save_data_csv.py` | Acquire and save one measurement loop to CSV |
| `001d.multi_loop_csv.py` | Acquire multiple loops to CSV |
| `Fisens_batch_file/batch.bat` / `batch.txt` | Batch script used to run the software |

## Setup

1. Create a virtual environment and install the requirements:
   ```
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt  # Raspberry Pi: requirements_fisens_rpi.txt
   ```
2. Create an `apikey.env` file in the project folder (it is ignored by git) with your InfluxDB token:
   ```
   INFLUXDB_TOKEN=<your token>
   ```
3. Set the serial port (for example `/dev/ttyUSB0` or `COM3`), the InfluxDB URL and organisation, and the project path in the scripts. The scripts still contain example paths such as `/path/to/001_automation_fisens_influxdb`.

## Notes

- Never commit `apikey.env` or other tokens.
- The LabVIEW code is on the `2026` branch; earlier scripts (test and system checks) are on the `2025` branch.
