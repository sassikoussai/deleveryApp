# Docker Setup for Microservices

This project is containerized and can be run with a single Docker Compose command.

## Prerequisites

- Docker Desktop installed and running
- At least 4GB of RAM available for Docker

## Quick Start

### Windows (PowerShell)

**Start all services:**
```powershell
.\start-services.ps1
```

**Or manually:**
```powershell
docker-compose up -d --build
```

**Stop all services:**
```powershell
.\stop-services.ps1
```

**Or manually:**
```powershell
docker-compose down
```

### Linux/Mac

```bash
docker-compose up -d --build
```

## Service URLs

Once all services are running:

- **Eureka Server**: http://localhost:8761
- **API Gateway**: http://localhost:8089
- **User Service**: http://localhost:8082
- **Restaurant Service**: http://localhost:8083
- **Order Delivery Service**: http://localhost:8000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

## Service Startup Order

Services start in the following order (enforced by dependencies):

1. **Eureka Server** - Service discovery (must start first)
2. **User Service** - Waits for Eureka
3. **Restaurant Service** - Waits for Eureka
4. **Order Delivery Service** - Waits for Eureka
5. **API Gateway** - Waits for all services to be healthy
6. **Prometheus** - Monitoring
7. **Grafana** - Visualization

## Useful Commands

### View Logs

**All services:**
```powershell
docker-compose logs -f
```

**Specific service:**
```powershell
docker-compose logs -f eureka-server
docker-compose logs -f user-service
docker-compose logs -f gateway
```

### Check Service Status

```powershell
docker-compose ps
```

### Restart a Service

```powershell
docker-compose restart user-service
```

### Rebuild a Service

```powershell
docker-compose up -d --build user-service
```

### Access Service Shell

```powershell
docker exec -it user-service sh
```

## Database Persistence

SQLite databases are stored in Docker volumes:
- `user-service-db` - User Service database
- `restaurant-service-db` - Restaurant Service database
- `order-delivery-db` - Order Delivery Service database

To remove all data:
```powershell
docker-compose down -v
```

## Troubleshooting

### Services Not Starting

1. **Check Docker is running:**
   ```powershell
   docker ps
   ```

2. **Check service logs:**
   ```powershell
   docker-compose logs [service-name]
   ```

3. **Check service health:**
   ```powershell
   docker-compose ps
   ```

### Port Already in Use

If a port is already in use, either:
- Stop the service using that port
- Change the port mapping in `docker-compose.yml`

### Services Can't Connect to Eureka

1. Wait for Eureka to be healthy (check with `docker-compose ps`)
2. Check Eureka logs: `docker-compose logs eureka-server`
3. Verify network: `docker network ls`

### Database Issues

If databases are corrupted:
```powershell
docker-compose down -v
docker-compose up -d --build
```

This will recreate all databases from scratch.

## Development Mode

For development, you can still run services locally (outside Docker) while others run in Docker. Just make sure to:

1. Update `application.properties` to use `localhost:8761` for Eureka
2. Ensure Eureka is running in Docker first
3. Services will register with Docker Eureka instance

## Production Considerations

For production deployment, consider:
- Using external databases (PostgreSQL, MySQL) instead of SQLite
- Setting up proper secrets management
- Configuring resource limits
- Setting up health checks and auto-restart policies
- Using Docker Swarm or Kubernetes for orchestration

