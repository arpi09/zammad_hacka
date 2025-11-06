# Quick Start: Using Zammad API in Grafana Dashboards

## Step 1: Verify Datasource (30 seconds)

1. Open Grafana: http://localhost:3001
2. Login: `admin` / `admin`
3. Go to **Configuration** (gear icon) → **Data Sources**
4. Click on **"Zammad API"**
5. Click **"Save & Test"** - should show green "Data source is working"

## Step 2: Create Your First Panel (2 minutes)

### Option A: Create New Dashboard

1. Click **+** (plus icon) → **Create Dashboard**
2. Click **Add visualization** (or **Add** → **Visualization**)
3. In the query editor:
   - **Data source**: Select **"Zammad API"** from dropdown
   - **Query type**: Leave as default
   - **Target**: Type one of these:
     - `tickets_timeseries` ← For line graphs showing tickets over time
     - `tickets_by_state` ← For pie/bar charts by state
     - `tickets_by_priority` ← For pie/bar charts by priority
4. Click **Run query** button (top right)
5. You should see data appear!

### Option B: Add to Existing Dashboard

1. Open any dashboard
2. Click **Add** → **Visualization**
3. Follow steps 3-5 from Option A

## Step 3: Choose Visualization Type

After you see data, select a visualization type:

- **Time series** - Best for `tickets_timeseries`
- **Pie chart** - Best for `tickets_by_state` or `tickets_by_priority`
- **Bar gauge** - Good for state/priority data
- **Stat** - Shows a single number

## Available Targets/Metrics

When creating a query, use these in the "Target" field:

| Target | What it shows | Best visualization |
|--------|---------------|-------------------|
| `tickets_timeseries` | Tickets created over time | Time series, Line chart |
| `tickets_by_state` | Count of tickets by state (open, closed, etc.) | Pie chart, Bar chart |
| `tickets_by_priority` | Count of tickets by priority | Pie chart, Bar chart |

## Troubleshooting

### "No data" appears
- Check backend is running: http://localhost:8000/health
- Verify datasource: Configuration → Data Sources → Zammad API → Save & Test
- Make sure you typed the target name correctly (case-sensitive)

### "Datasource not found"
- Go to Configuration → Data Sources
- Check if "Zammad API" is listed
- If not, add it:
  - Click "Add data source"
  - Search for "Simple JSON"
  - URL: `http://backend:8000/api/v1/grafana`
  - Access: Server

### Can't see "Zammad API" in datasource dropdown
- The Simple JSON plugin might need a restart
- Try refreshing the page
- Or restart Grafana: `docker restart zammad-grafana-local`

## Example: Create a Time Series Graph

1. New dashboard → Add visualization
2. Data source: **Zammad API**
3. Target: `tickets_timeseries`
4. Visualization: **Time series**
5. Click **Run query**
6. You should see a graph!

## Example: Create a Pie Chart

1. New dashboard → Add visualization
2. Data source: **Zammad API**
3. Target: `tickets_by_state`
4. Visualization: **Pie chart**
5. Click **Run query**
6. You should see a pie chart!

That's it! You're now using the Zammad API in Grafana! 🎉

