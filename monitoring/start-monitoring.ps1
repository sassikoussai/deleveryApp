# PowerShell script to start Prometheus and Grafana with Docker

Write-Host "Starting Prometheus and Grafana monitoring stack..." -ForegroundColor Green

# Check if Docker is running
try {
    docker ps | Out-Null
    Write-Host "Docker is running" -ForegroundColor Green
} catch {
    Write-Host "Error: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Navigate to monitoring directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Start services
Write-Host "`nStarting Docker containers..." -ForegroundColor Yellow
docker-compose up -d

# Wait a moment for services to start
Start-Sleep -Seconds 3

# Check if containers are running
$prometheusStatus = docker ps --filter "name=prometheus" --format "{{.Status}}"
$grafanaStatus = docker ps --filter "name=grafana" --format "{{.Status}}"

Write-Host "`n=== Monitoring Services Status ===" -ForegroundColor Cyan
Write-Host "Prometheus: $prometheusStatus" -ForegroundColor $(if ($prometheusStatus) { "Green" } else { "Red" })
Write-Host "Grafana: $grafanaStatus" -ForegroundColor $(if ($grafanaStatus) { "Green" } else { "Red" })

Write-Host "`n=== Access URLs ===" -ForegroundColor Cyan
Write-Host "Prometheus: http://localhost:9090" -ForegroundColor Yellow
Write-Host "Grafana: http://localhost:3001" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor Gray
Write-Host "  Password: admin" -ForegroundColor Gray

Write-Host "`n=== Useful Commands ===" -ForegroundColor Cyan
Write-Host "View logs: docker-compose logs -f" -ForegroundColor Gray
Write-Host "Stop services: docker-compose down" -ForegroundColor Gray
Write-Host "Restart services: docker-compose restart" -ForegroundColor Gray

Write-Host "`nMonitoring stack started successfully!" -ForegroundColor Green

