# Creating Your First Grafana Dashboard

## Step-by-Step Guide

### Step 1: Create New Dashboard

1. In Grafana, click **+** (plus icon) in the left sidebar
2. Click **"Create Dashboard"**
3. Click **"Add visualization"** (or **"Add"** → **"Visualization"**)

### Step 2: Select Data Source

1. In the query editor, click the dropdown that says "Select data source" or shows a datasource name
2. Select **"Zammad API"** (your Prometheus datasource)

### Step 3: Write Your First Query

In the query editor (PromQL), type one of these:

**Simple metrics:**
- `zammad_tickets_total` - Total number of tickets
- `zammad_tickets_open` - Open tickets
- `zammad_tickets_closed` - Closed tickets

**Grouped metrics:**
- `zammad_tickets_by_state` - All tickets grouped by state
- `zammad_tickets_by_priority` - All tickets grouped by priority

### Step 4: Choose Visualization

After entering the query, click **"Run query"** (top right), then select a visualization type:

- **Stat** - Shows a single number (great for `zammad_tickets_total`)
- **Time series** - Line graph over time
- **Bar gauge** - Horizontal bars
- **Pie chart** - For grouped data like `zammad_tickets_by_state`
- **Table** - Tabular data

### Step 5: Customize Panel

1. Click the panel title to edit
2. Change title, add descriptions
3. Adjust colors, thresholds, etc.

### Step 6: Save Dashboard

1. Click **"Save dashboard"** (top right)
2. Enter a name: "Zammad Overview"
3. Click **"Save"**

## Example Dashboard Panels

### Panel 1: Total Tickets (Stat)
- Query: `zammad_tickets_total`
- Visualization: **Stat**
- Shows: Total number of tickets

### Panel 2: Tickets by State (Pie Chart)
- Query: `zammad_tickets_by_state`
- Visualization: **Pie chart**
- Shows: Distribution of tickets by state

### Panel 3: Tickets by Priority (Bar Gauge)
- Query: `zammad_tickets_by_priority`
- Visualization: **Bar gauge**
- Shows: Tickets grouped by priority

### Panel 4: Open vs Closed (Stat)
- Query: `zammad_tickets_open` and `zammad_tickets_closed`
- Visualization: **Stat** (multiple queries)
- Shows: Comparison of open and closed tickets

## Tips

- Use **"Run query"** frequently to see your data
- Click **"Explore"** to test queries before adding to dashboard
- Use **"Transform"** tab to format data if needed
- Add multiple queries to one panel for comparisons

