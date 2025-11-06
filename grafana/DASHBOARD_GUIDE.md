# How to Use Zammad API in Grafana Dashboards

## Step 1: Verify Datasource is Configured

1. In Grafana, go to **Configuration** → **Data Sources**
2. You should see "Zammad API" listed
3. Click on it to verify it's configured correctly
4. Click "Save & Test" - it should show "Data source is working"

## Step 2: Install Simple JSON Datasource Plugin (if needed)

If the datasource shows an error, you may need to install the plugin:

```bash
# In Docker container
docker exec zammad-grafana-local grafana-cli plugins install grafana-simple-json-datasource
docker restart zammad-grafana-local
```

Or in Grafana UI:
1. Go to **Configuration** → **Plugins**
2. Search for "Simple JSON"
3. Click "Install"

## Step 3: Create a Dashboard Panel

### Method 1: Create New Dashboard

1. Click **+** → **Create Dashboard**
2. Click **Add visualization**
3. In the query editor:
   - **Data source**: Select "Zammad API"
   - **Query type**: Select "Metrics"
   - **Target**: Enter one of these:
     - `tickets_timeseries` - For time-series graphs
     - `tickets_by_state` - For tickets grouped by state
     - `tickets_by_priority` - For tickets grouped by priority
4. Click **Run query** to see the data
5. Choose visualization type (Graph, Pie Chart, Bar Gauge, etc.)

### Method 2: Add Panel to Existing Dashboard

1. Open your dashboard
2. Click **Add** → **Visualization**
3. Follow steps 3-5 from Method 1

## Available Metrics/Targets

When creating a panel, use these targets in the query:

- **`tickets_timeseries`** - Time-series data showing tickets created over time
  - Best for: Time series graphs, line charts
  - Returns: `[{"target": "Tickets Created", "datapoints": [[value, timestamp], ...]}]`

- **`tickets_by_state`** - Tickets grouped by state (open, closed, etc.)
  - Best for: Pie charts, bar charts, stat panels
  - Returns: `[{"state": "open", "count": 10}, ...]`

- **`tickets_by_priority`** - Tickets grouped by priority
  - Best for: Pie charts, bar charts, stat panels
  - Returns: `[{"priority": "high", "count": 5}, ...]`

## Example Panel Configurations

### Time Series Graph (Tickets Over Time)

1. **Visualization**: Time series
2. **Data source**: Zammad API
3. **Target**: `tickets_timeseries`
4. **Format**: Time series

### Pie Chart (Tickets by State)

1. **Visualization**: Pie chart
2. **Data source**: Zammad API
3. **Target**: `tickets_by_state`
4. **Format**: Table (may need to transform)

### Stat Panel (Total Tickets)

1. **Visualization**: Stat
2. **Data source**: Zammad API
3. **Target**: `tickets_timeseries`
4. **Calculation**: Last value or Sum

## Troubleshooting

### "No data" or "Query failed"

1. Check backend is running: `http://localhost:8000/health`
2. Test datasource: Configuration → Data Sources → Zammad API → Save & Test
3. Check backend logs for errors
4. Verify the target/metric name is correct

### "Datasource not found"

1. Go to Configuration → Data Sources
2. Check if "Zammad API" exists
3. If not, add it manually:
   - Type: Simple JSON
   - URL: `http://backend:8000/api/v1/grafana` (in Docker) or `http://localhost:8000/api/v1/grafana` (local)
   - Access: Server

### Data format issues

The Simple JSON datasource expects specific formats. If your data doesn't display correctly:
- For time series: Ensure data is in `[[value, timestamp], ...]` format
- For tables: May need to use Transform tab to format data

## Quick Test Query

To test if everything works:

1. Create a new panel
2. Data source: Zammad API
3. Target: `tickets_timeseries`
4. Click "Run query"
5. You should see data points if backend has ticket data

