# Fix Grafana Dashboard - No Data Issue

## Problem
Queries work in Explore but dashboards show no data. This is because:
- Your metrics have `application="USER-SERVICE"` label
- Prometheus adds `instance="host.docker.internal:8082"` label
- Dashboards might be filtering by wrong labels

## Solution: Fix Dashboard Variable and Queries

### Step 1: Check Current Dashboard Variable

1. Go to your dashboard
2. Click **Settings** (gear icon) → **Variables**
3. Check the "Instance" variable:
   - **Query**: Should be `label_values(up, instance)`
   - **Current value**: Should show `host.docker.internal:8082`

### Step 2: Fix Dashboard Queries

The issue is that Spring Boot 3 metrics use `application` label, but Prometheus adds `instance` label. You need to filter by BOTH or use the correct one.

**Option A: Filter by instance (Recommended)**

Edit each panel query to use:
```
process_uptime_seconds{instance="$instance"}
```

**Option B: Filter by application label**

If the dashboard uses `application` label, you need to:
1. Create an "Application" variable:
   - Name: `application`
   - Query: `label_values(jvm_memory_used_bytes, application)`
2. Update queries to: `process_uptime_seconds{application="$application",instance="$instance"}`

### Step 3: Quick Fix - Edit Dashboard JSON

1. Click **Settings** → **JSON Model**
2. Find queries like: `process_uptime_seconds{application=~"$application"}`
3. Replace with: `process_uptime_seconds{instance="$instance"}`
4. Or add both filters: `process_uptime_seconds{instance="$instance",application=~".*"}`

### Step 4: Test Each Panel

For each panel showing "No data":
1. Click **Edit** on the panel
2. Go to **Query** tab
3. Check the query - it should include `instance="$instance"`
4. Test the query - click the query inspector icon
5. If it returns data, the panel should update

## Common Query Fixes

### Uptime
**Wrong:** `process_uptime_seconds{application=~"$application"}`
**Correct:** `process_uptime_seconds{instance="$instance"}`

### Memory
**Wrong:** `jvm_memory_used_bytes{application=~"$application",area="heap"}`
**Correct:** `sum(jvm_memory_used_bytes{instance="$instance",area="heap"})`

### CPU
**Wrong:** `process_cpu_usage{application=~"$application"}`
**Correct:** `process_cpu_usage{instance="$instance"} * 100`

### HTTP Requests
**Wrong:** `rate(http_server_requests_seconds_count{application=~"$application"}[5m])`
**Correct:** `rate(http_server_requests_seconds_count{instance="$instance"}[5m])`

## Alternative: Use Application Variable

If you want to filter by application name:

1. Add a new variable:
   - Name: `application`
   - Type: `Query`
   - Query: `label_values(jvm_memory_used_bytes, application)`
   - Multi-value: Yes (optional)

2. Update queries to use both:
   ```
   process_uptime_seconds{instance="$instance",application=~"$application"}
   ```

## Import Working Dashboard

I've created a working dashboard JSON file: `spring-boot-3-dashboard.json`

To import:
1. Grafana → **Dashboards** → **Import**
2. Click **Upload JSON file**
3. Select `monitoring/spring-boot-3-dashboard.json`
4. Select Prometheus data source
5. Click **Import**

This dashboard uses `instance` variable correctly and should work immediately.

