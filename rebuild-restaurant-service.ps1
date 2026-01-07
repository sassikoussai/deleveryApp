# Rebuild and restart restaurant service
Write-Host "Rebuilding restaurant-service..." -ForegroundColor Yellow
docker-compose build restaurant-service

Write-Host "Restarting restaurant-service..." -ForegroundColor Yellow
docker-compose up -d restaurant-service

Write-Host "Waiting for service to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host "Checking service status..." -ForegroundColor Yellow
docker-compose ps restaurant-service

Write-Host "`nService should be ready. Test with:" -ForegroundColor Green
Write-Host "http://localhost:8089/api/restaurants/menu-items/by-restaurant/1" -ForegroundColor Cyan

