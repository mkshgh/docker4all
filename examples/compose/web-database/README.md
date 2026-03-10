# Web + Database Compose Example

A complete Docker Compose example with web server and database.

## What This Demonstrates

- Docker Compose v2 syntax (compose.yaml)
- Multi-container application
- Service dependencies
- Custom networks
- Named volumes for data persistence
- Health checks
- Port mapping
- Environment variables

## Services

### Web (Nginx)
- Serves static HTML
- Accessible at http://localhost:8080
- Depends on database service

### Database (PostgreSQL)
- PostgreSQL 15
- Persistent data storage
- Health check configured
- Isolated on custom network

## How to Run

```bash
# Start all services
docker compose up

# Start in background
docker compose up -d

# View logs
docker compose logs
docker compose logs web
docker compose logs db

# Check status
docker compose ps

# Stop services
docker compose down

# Stop and remove volumes (deletes database data)
docker compose down -v
```

## Accessing the Application

Open your browser to: http://localhost:8080

## Testing Database Connection

```bash
# Connect to database
docker compose exec db psql -U appuser -d myapp

# Inside psql:
\l              # List databases
\dt             # List tables
\q              # Quit
```

## File Structure

```
web-database/
├── compose.yaml       # Compose configuration
├── html/
│   └── index.html    # Web content
└── README.md         # This file
```

## Key Concepts

### Service Dependencies

```yaml
depends_on:
  - db
```

Web service waits for database to start.

### Named Volumes

```yaml
volumes:
  db-data:/var/lib/postgresql/data
```

Data persists even after `docker compose down`.

### Custom Networks

```yaml
networks:
  app-network:
    driver: bridge
```

Services communicate on isolated network.

### Health Checks

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U appuser"]
```

Monitors database health.

## Troubleshooting

### Port Already in Use

Change the port in compose.yaml:
```yaml
ports:
  - "8081:80"  # Use 8081 instead
```

### Database Connection Failed

Check database is healthy:
```bash
docker compose ps
docker compose logs db
```

### Permission Denied

Ensure Docker is running and you have permissions:
```bash
docker compose ps
```

## Next Steps

- Modify the HTML content
- Add more services (Redis, etc.)
- Learn about [Docker Compose](../../docs/04-compose/01-compose-introduction.md)
- Explore [Networking](../../docs/05-networking/01-networking-basics.md)
