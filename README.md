# FiSens Fiber Optic Sensor – Data Logging and Dashboard

Current Python scripts and Windows batch files for the FiSens fibre optic sensor: serial acquisition, InfluxDB logging, a web dashboard, and Docker setup.

## Files

| File | Purpose |
|---|---|
| `Fiber_optic_sensing_60sec.py` | Read the sensor over the serial port every 60 seconds and write to InfluxDB |
| `fisens_dashboard.py` | Web dashboard that reads from InfluxDB (uses `templates/index.html`) |
| `clear_com_port.py` | Clear the serial port |
| `clear_influxdb.py` | Delete all data from the `sensors` bucket (asks for confirmation) |
| `start_single_session.bat` | Start one logging session on Windows |
| `start_dashboard.bat` | Start the dashboard on Windows |
| `Dockerfile`, `docker-compose.yml` | Run the services in Docker |
| `requirements.txt` | Python dependencies |

## Setup

1. Create a virtual environment and install the requirements:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Set the InfluxDB token as an environment variable named `INFLUXDB_TOKEN` (or in a `.env` file, which git ignores). The org is `fisens` and the bucket is `sensors`.
3. Set `INFLUXDB_PASSWORD` and `GRAFANA_PASSWORD` in your environment or `.env`. Docker Compose refuses to start until both are set.

## Notes

- Never commit `.env`, `influx_api.txt`, or other tokens. They are listed in `.gitignore`.
- Older 2025 scripts and the LabVIEW code are on the `2025` and `2026` branches.
