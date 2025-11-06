# Prometheus Datasource Setup for Windows Server Grafana

## Why Prometheus?
- **Built into Grafana** - No plugins needed!
- Works with all Grafana versions
- Native support for time-series data

## Setup Instructions

### In Windows Server Grafana:

1. **Go to:** Configuration → Data Sources (or Connections → Data Sources)

2. **Click:** "Add new data source"

3. **Select:** "Prometheus" (it's in the list, no search needed)

4. **Configure:**
   - **Name:** `Zammad API` (or any name you prefer)
   - **URL:** `http://10.50.0.134:8000/api/v1/prometheus`
   - **Access:** Server (default)
   - Leave other settings as default

5. **Click:** "Save & Test"
   - Should show: "Data source is working"

## Available Metrics

After connecting, you can query these metrics:

- `zammad_tickets_total` - Total number of tickets
- `zammad_tickets_open` - Number of open tickets
- `zammad_tickets_closed` - Number of closed tickets
- `zammad_tickets_by_state{state="open"}` - Tickets by state
- `zammad_tickets_by_priority{priority="high"}` - Tickets by priority

## Creating Dashboards

1. Create new dashboard
2. Add panel
3. Select "Zammad API" (Prometheus) as datasource
4. In query editor, use PromQL:
   - `zammad_tickets_total`
   - `zammad_tickets_open`
   - `zammad_tickets_by_state`
5. Choose visualization (Graph, Stat, etc.)

## Example Queries

- `zammad_tickets_total` - Shows total tickets
- `zammad_tickets_open` - Shows open tickets
- `zammad_tickets_by_state` - Shows all tickets grouped by state
- `zammad_tickets_by_priority` - Shows all tickets grouped by priority

That's it! Prometheus is built-in, so it will definitely work!

