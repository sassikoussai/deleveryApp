# Monitoring Setup with Prometheus and Grafana

This directory contains the configuration files for monitoring your microservices using Prometheus and Grafana.

## Quick Start with Docker

### Windows (PowerShell)

**Option 1: Use the startup script (Recommended)**
```powershell
cd monitoring
.\start-monitoring.ps1
```

**Option 2: Manual start**
```powershell
cd monitoring
docker-compose up -d
```

**To stop:**
```powershell
.\stop-monitoring.ps1
# or
docker-compose down
```

### Linux/Mac

```bash
cd monitoring
docker-compose up -d
```

### Access the services:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001
  - Username: `admin`
  - Password: `admin`

3. **Verify metrics endpoints:**
   - User Service: http://localhost:8082/actuator/prometheus
   - Restaurant Service: http://localhost:8083/actuator/prometheus
   - Gateway: http://localhost:8089/actuator/prometheus
   - Eureka: http://localhost:8761/actuator/prometheus
   - Order Service: http://localhost:8000/actuator/prometheus

## Manual Setup (Without Docker)

### Prometheus

1. Download Prometheus from https://prometheus.io/download/
2. Extract and run:
   ```bash
   prometheus.exe --config.file=prometheus-local.yml
   ```
3. Access at http://localhost:9090

### Grafana

1. Download Grafana from https://grafana.com/grafana/download
2. Install and start Grafana
3. Access at http://localhost:3000 (default: admin/admin)
4. Add Prometheus data source:
   - URL: http://localhost:9090
   - Save & Test

## Grafana Dashboard Setup

1. **Add Prometheus Data Source:**
   - Go to Configuration → Data Sources
   - Add Prometheus
   - URL: http://prometheus:9090 (Docker) or http://localhost:9090 (Local)
   - Save & Test

2. **Import Dashboards:**
   - Go to Dashboards → Import
   - Use Dashboard ID: `11378` (Spring Boot 2.1 Statistics)
   - Or create custom dashboards using the metrics

## Available Metrics

### Spring Boot Services (User, Restaurant, Gateway, Eureka)
- `http_server_requests_seconds` - HTTP request duration
- `jvm_memory_used_bytes` - JVM memory usage
- `jvm_gc_pause_seconds` - Garbage collection metrics
- `process_cpu_usage` - CPU usage
- `system_cpu_usage` - System CPU usage

### Django Service (Order Delivery)
- `http_requests_total` - Total HTTP requests by method, endpoint, status
- `http_request_duration_seconds` - HTTP request duration
- `orders_created_total` - Total orders created
- `deliveries_created_total` - Total deliveries created
- `active_orders` - Number of active orders
- `active_deliveries` - Number of active deliveries

## Troubleshooting

- **Metrics not appearing:** Ensure all services are running and accessible
- **Connection refused:** Check that services are running on the correct ports
- **Docker networking:** Use `host.docker.internal` for Windows/Mac to access host services

