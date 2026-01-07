# PowerShell script to start all microservices with Docker Compose

Write-Host "Starting all microservices with Docker Compose..." -ForegroundColor Green

# Check if Docker is running
try {
    docker ps | Out-Null
    Write-Host "Docker is running" -ForegroundColor Green
} catch {
    Write-Host "Error: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Navigate to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Build and start services
Write-Host "`nBuilding and starting services..." -ForegroundColor Yellow
docker-compose up -d --build

# Wait a moment for services to start
Start-Sleep -Seconds 5

# Check service status
Write-Host "`n=== Service Status ===" -ForegroundColor Cyan
docker-compose ps

Write-Host "`n=== Service URLs ===" -ForegroundColor Cyan
Write-Host "Eureka Server: http://localhost:8761" -ForegroundColor Yellow
Write-Host "API Gateway: http://localhost:8089" -ForegroundColor Yellow
Write-Host "User Service: http://localhost:8082" -ForegroundColor Yellow
Write-Host "Restaurant Service: http://localhost:8083" -ForegroundColor Yellow
Write-Host "Order Delivery Service: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Prometheus: http://localhost:9090" -ForegroundColor Yellow
Write-Host "Grafana: http://localhost:3001 (admin/admin)" -ForegroundColor Yellow

Write-Host "`n=== Useful Commands ===" -ForegroundColor Cyan
Write-Host "View logs: docker-compose logs -f [service-name]" -ForegroundColor Gray
Write-Host "Stop services: docker-compose down" -ForegroundColor Gray
Write-Host "Restart a service: docker-compose restart [service-name]" -ForegroundColor Gray
Write-Host "View all logs: docker-compose logs -f" -ForegroundColor Gray

Write-Host "`nServices are starting. Please wait for all services to be healthy..." -ForegroundColor Green
Write-Host "Check service health with: docker-compose ps" -ForegroundColor Gray

