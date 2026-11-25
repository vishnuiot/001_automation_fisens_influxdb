# FiSens InfluxDB Automation – Python Data Logging (2025)

This branch (`2025`) holds the Python scripts used in 2025 to read fibre optic sensor data from the FiSens / FiSpec interrogator over a serial port, save it to CSV, and write it to InfluxDB. The current LabVIEW work is on `main` and `2026`.

## Scripts

| File | Purpose |
|---|---|
| `001.test.py` | Quick serial communication test |
| `001a.get_system_parameters_fullyworking.py` | Read interrogator system parameters |
| `001aa.raspberrypi_get_system_parameters.py` | Same, for a Raspberry Pi |
| `001b.fullyworking_systemcommands.py` | Send system commands to the interrogator |
| `001c.single_loop_save_data_csv.py` | Acquire and save one measurement loop to CSV |
| `001d.multi_loop_csv.py` | Acquire multiple loops to CSV |
| `002a_max_point_influxdb.py` | Acquire peak data and write to InfluxDB |
| `002aa_raspberrypi_max_point_influxdb copy.py` | Raspberry Pi version of the InfluxDB logger |
| `003.print_python_environment.py` | Print the Python environment for troubleshooting |
| `08.list_serial_ports.sh` | List serial ports |

## Setup

1. Create a virtual environment and install the requirements:
   ```
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt  # Raspberry Pi: requirements_fisens_rpi.txt
   ```
2. Create an `apikey.env` file in the project folder (it is ignored by git) with your InfluxDB settings:
   ```
   INFLUXDB_TOKEN=<your token>
   ```
3. Set the serial port (for example `/dev/ttyUSB0`), the InfluxDB URL and organisation, and the project path in the scripts. Some scripts still contain example paths such as `/path/to/001_automation_fisens_influxdb`.

## Notes

- Never commit `apikey.env` or other tokens.
- `.venv/` and LibreOffice lock files (`.~lock*`) are not part of the project.
