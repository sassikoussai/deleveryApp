# PowerShell script to stop Prometheus and Grafana

Write-Host "Stopping Prometheus and Grafana monitoring stack..." -ForegroundColor Yellow

# Navigate to monitoring directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Stop services
docker-compose down

Write-Host "Monitoring stack stopped." -ForegroundColor Green

