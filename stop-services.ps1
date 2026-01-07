# PowerShell script to stop all microservices

Write-Host "Stopping all microservices..." -ForegroundColor Yellow

# Navigate to project directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Stop services
docker-compose down

Write-Host "All services stopped." -ForegroundColor Green

