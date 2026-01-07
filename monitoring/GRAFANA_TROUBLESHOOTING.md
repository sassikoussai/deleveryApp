# Grafana Dashboard Troubleshooting Guide

## Issue: Dashboard Shows No Data Despite Metrics Being Available

The Spring Boot Statistics dashboard (ID: 12464) was designed for Spring Boot 2.x, but you're using Spring Boot 3.3.5+. The metric names and labels have changed.

## Available Metrics in Your Services

Based on the metrics endpoint, here are the key metrics available:

### Uptime
- `process_uptime_seconds{application="USER-SERVICE"}` ✓

### Memory
- `jvm_memory_used_bytes{application="USER-SERVICE",area="heap",id="G1 Eden Space"}` ✓
- `jvm_memory_used_bytes{application="USER-SERVICE",area="heap",id="G1 Old Gen"}` ✓
- `jvm_memory_used_bytes{application="USER-SERVICE",area="nonheap",id="Metaspace"}` ✓

### CPU
- `process_cpu_usage{application="USER-SERVICE"}` ✓
- `system_cpu_usage{application="USER-SERVICE"}` ✓

### HTTP Requests
- `http_server_requests_seconds_count{application="USER-SERVICE",uri="/users"}` ✓
- `http_server_requests_seconds_sum{application="USER-SERVICE",uri="/users"}` ✓

## Quick Fix: Test Queries in Grafana Explore

1. Go to Grafana → **Explore** (compass icon)
2. Select **Prometheus** data source
3. Try these queries one by one:

### Test Uptime
```
process_uptime_seconds{instance="host.docker.internal:8082"}
```

### Test Memory (Heap)
```
sum(jvm_memory_used_bytes{instance="host.docker.internal:8082",area="heap"})
```

### Test CPU
```
process_cpu_usage{instance="host.docker.internal:8082"}
```

### Test HTTP Requests
```
rate(http_server_requests_seconds_count{instance="host.docker.internal:8082"}[5m])
```

If these queries work in Explore, the issue is with the dashboard queries.

## Solution Options

### Option 1: Use a Spring Boot 3 Compatible Dashboard

Try these dashboard IDs:
- **6756** - Spring Boot Statistics (more compatible)
- **14430** - Spring Boot Statistics & Endpoint Metrics

### Option 2: Fix the Current Dashboard Queries

The dashboard queries likely need to:
1. Filter by `instance` label (which you've fixed)
2. May need to filter by `application` label instead of or in addition to `instance`
3. Use correct metric names for Spring Boot 3

### Option 3: Create a Custom Simple Dashboard

1. In Grafana, click **+** → **Create Dashboard**
2. Add panels with these queries:

**Uptime Panel:**
```
process_uptime_seconds{instance="$instance"}
```

**Memory Used Panel:**
```
sum(jvm_memory_used_bytes{instance="$instance",area="heap"})
```

**CPU Usage Panel:**
```
process_cpu_usage{instance="$instance"} * 100
```

**HTTP Request Rate:**
```
rate(http_server_requests_seconds_count{instance="$instance"}[5m])
```

## Common Issues

1. **Label Mismatch**: Dashboard might be looking for `job` label but your metrics use `application` label
2. **Metric Name Changes**: Spring Boot 3 uses different metric names
3. **Label Filters**: Dashboard queries might filter by labels that don't exist in your metrics

## Verify Your Metrics

Check what labels your metrics actually have:
1. Go to Prometheus: http://localhost:9090
2. Run: `up{job="user-service"}`
3. Check all the labels shown
4. Make sure dashboard queries use the same labels

