# Grafana dashboard – data source ID

The dashboard `Real_Time_Fiber_Optic_Sensing_System.json` reads from InfluxDB through a data source with the ID:

```
dg1x9xhe8xg5cd
```

Use this same ID for the InfluxDB data source both locally and in any GitHub or Docker setup. If the ID is different, the panels show "No data" or an error until you edit each panel's data source.

To check or set it in Grafana: **Connections → Data sources → InfluxDB**, then look at the ID in the browser address bar (`/connections/datasources/edit/<ID>`).
