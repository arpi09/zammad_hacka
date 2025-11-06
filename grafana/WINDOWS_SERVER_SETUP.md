# Setting Up Windows Server Grafana with Local Backend

## Step 2 Explained: Connect Windows Server Grafana to Your Local Backend

### What You Need:
1. Your local computer's IP address (where backend is running)
2. Backend running on port 8000
3. Windows server Grafana with Simple JSON plugin

### Detailed Steps:

#### Step 1: Find Your Local IP Address
Your local IP is: **CHECK THE OUTPUT ABOVE** (usually something like 192.168.x.x or 10.x.x.x)

#### Step 2: Make Sure Backend is Accessible
- Your backend is running at: `http://localhost:8000`
- For Windows server to access it, use: `http://YOUR_LOCAL_IP:8000`
- Example: `http://192.168.1.100:8000`

#### Step 3: Configure Windows Server Grafana

1. **Open your Windows server Grafana** (the one that has Simple JSON plugin working)

2. **Go to Configuration → Data Sources** (or Connections → Data Sources)

3. **Click "Add new data source"**

4. **Search for "Simple JSON"** and select it

5. **Configure the datasource:**
   - **Name:** `Zammad API Local` (or any name you prefer)
   - **URL:** `http://YOUR_LOCAL_IP:8000/api/v1/grafana`
     - Replace `YOUR_LOCAL_IP` with your actual IP (from step 1)
     - Example: `http://192.168.1.100:8000/api/v1/grafana`
   - **Access:** Server (default)
   - **HTTP Method:** GET

6. **Click "Save & Test"**
   - Should show: "Data source is working"

#### Step 4: Create Dashboards
Now you can create dashboards in Windows server Grafana using:
- Target: `tickets_timeseries`
- Target: `tickets_by_state`
- Target: `tickets_by_priority`

### Troubleshooting:

**If "Save & Test" fails:**
- Check Windows Firewall on your local machine - port 8000 might be blocked
- Make sure backend is running: `http://localhost:8000/health`
- Try accessing from Windows server browser: `http://YOUR_LOCAL_IP:8000/health`

**If you can't find Simple JSON plugin:**
- Install it: `grafana-cli plugins install grafana-simple-json-datasource`
- Restart Grafana

**Alternative: If Simple JSON doesn't work on Windows server either:**
- Use the React frontend at `http://YOUR_LOCAL_IP:5173` from Windows server
- Or deploy backend to a server both can access

