# Fix: Grafana Datasource Issue

## Problem
The "Simple JSON" datasource plugin is deprecated (Angular-based) and doesn't work with Grafana 12+.

## Solution: Use Built-in Datasources

### Option 1: Use InfluxDB Datasource (Recommended)

1. **Delete the broken datasource:**
   - Click on "Zammad API" datasource
   - Click "Delete" button at the bottom
   - Confirm deletion

2. **Add InfluxDB datasource:**
   - Click "Add new data source"
   - Search for "InfluxDB"
   - Configure:
     - **Name:** Zammad API
     - **Query Language:** Flux (or InfluxQL)
     - **URL:** `http://host.docker.internal:8000`
     - **Access:** Server
   - Click "Save & Test"

3. **Use the backend's InfluxDB-compatible endpoint** (we'll create this)

### Option 2: Use Direct API Queries (Simpler)

Instead of a datasource, you can:
1. Use Grafana's "Table" visualization
2. Manually query: `http://localhost:8000/api/v1/statistics/tickets`
3. Transform the JSON response in Grafana

### Option 3: Use TestData Datasource (For Testing)

1. Add "TestData" datasource (built-in)
2. Use it to test dashboard creation
3. Later connect to real data

## Quick Fix Right Now

**Simplest approach:**
1. Delete the "Zammad API" datasource
2. Create dashboards using manual API calls
3. Or wait for me to create InfluxDB-compatible endpoints

