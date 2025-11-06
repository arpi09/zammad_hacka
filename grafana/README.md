# Grafana Configuration

This directory contains Grafana configuration files for automatic provisioning.

**Note:** This setup is configured for **on-premises Grafana** (running in Docker). The backend API endpoints are generic and will also work with **Grafana Cloud** if your backend is publicly accessible.

## Structure

- `provisioning/datasources/` - Data source configurations (auto-configured on startup)
- `provisioning/dashboards/` - Dashboard provisioning configuration
- `dashboards/` - Dashboard JSON files

## Data Source

The Zammad API data source is automatically configured to connect to the backend API at:
- URL: `http://backend:8000/api/v1/grafana`

## Available Endpoints

The backend provides the following Grafana-compatible endpoints:

- `/query` - Main query endpoint (supports multiple targets)
- `/search` - Returns available metrics
- `/annotations` - For dashboard annotations
- `/tickets/timeseries` - Time-series data for tickets
- `/tickets/by-state` - Tickets grouped by state
- `/tickets/by-priority` - Tickets grouped by priority

## Using Grafana

1. Start the services with Docker Compose:
   ```bash
   docker-compose up
   ```

2. Access Grafana at `http://localhost:3001`
   - Username: `admin`
   - Password: `admin`

3. The "Zammad API" datasource should be automatically configured

4. Create dashboards using the available metrics:
   - `tickets_timeseries` - For time-series graphs
   - `tickets_by_state` - For pie/bar charts by state
   - `tickets_by_priority` - For pie/bar charts by priority

## Simple JSON Datasource Plugin

If using Grafana manually (not via Docker), you may need to install the "Simple JSON Datasource" plugin:

```bash
grafana-cli plugins install grafana-simple-json-datasource
```

Then restart Grafana.

