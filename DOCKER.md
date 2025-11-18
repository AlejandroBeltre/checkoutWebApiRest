# Docker Setup Documentation

## Overview

This project includes complete Docker support with automatic database creation and setup. The setup runs database migrations and creates an admin user automatically when the container starts.

## Key Features

- **Automatic Database Setup**: Database migrations run automatically on container startup
- **SQLite Support**: Default configuration with persistent storage
- **PostgreSQL Support**: Optional PostgreSQL configuration for production
- **Auto-created Admin User**: Admin user created automatically (username: `admin`, password: `admin123`)
- **Environment Variable Configuration**: Easily customize settings without code changes
- **Volume Persistence**: Database data persists across container restarts
- **Health Checks**: Built-in health monitoring for containers

## Architecture

### Dockerfile

The Dockerfile uses a multi-stage approach:
1. **Base Image**: Python 3.9-slim for smaller image size
2. **System Dependencies**: Installs gcc for Python package compilation
3. **Python Dependencies**: Installs all requirements including PostgreSQL support
4. **Application Setup**: Copies application code
5. **Entrypoint Script**: Configures runtime initialization
6. **Gunicorn Server**: Production-ready WSGI server with 3 workers

### Entrypoint Script

The `entrypoint.sh` script handles runtime initialization:
1. Waits for database connectivity
2. Runs Django migrations
3. Creates superuser if it doesn't exist
4. Collects static files
5. Starts the application server

### Database Configuration

**Settings.py** now supports:
- Environment variable configuration
- Both SQLite and PostgreSQL databases
- Automatic path resolution for Docker volumes
- Production-ready database settings

## Deployment Options

### Option 1: SQLite (Development/Testing)

Best for:
- Local development
- Testing
- Low-traffic applications
- Single-server deployments

```bash
# Using docker-compose
docker-compose up -d

# Using docker directly
mkdir -p data
docker build -t checkoutwebapi .
docker run -d -p 8000:8000 -v $(pwd)/data:/code/data checkoutwebapi
```

**Database Location**: `./data/db.sqlite3`

### Option 2: PostgreSQL (Production)

Best for:
- Production environments
- High-traffic applications
- Multi-server deployments
- Advanced database features

```bash
# Using docker-compose
docker-compose -f docker-compose.postgres.yml up -d
```

**Features**:
- Separate PostgreSQL container
- Persistent volume for database
- Health checks
- Service dependencies
- Automatic connection configuration

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | (insecure default) | Django secret key for sessions/crypto |
| `DJANGO_DEBUG` | `True` | Enable/disable debug mode |
| `DJANGO_ALLOWED_HOSTS` | `*` | Comma-separated list of allowed hosts |
| `DB_ENGINE` | `sqlite3` | Database engine (sqlite3/postgresql) |
| `DB_PATH` | `/code/data/db.sqlite3` | Path to SQLite database file |
| `DB_NAME` | `checkoutdb` | PostgreSQL database name |
| `DB_USER` | `postgres` | PostgreSQL username |
| `DB_PASSWORD` | `postgres` | PostgreSQL password |
| `DB_HOST` | `db` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |

### Using .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your values:
   ```bash
   DJANGO_SECRET_KEY=your-production-secret-key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

3. Use with docker-compose:
   ```bash
   docker-compose --env-file .env up -d
   ```

## Database Migrations

### Initial Setup

Migrations run automatically when the container starts. No manual intervention needed.

### Creating New Migrations

```bash
# Make migrations for model changes
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate
```

### Checking Migration Status

```bash
docker-compose exec web python manage.py showmigrations
```

## Data Persistence

### SQLite

Data persists in the `./data` directory:
- **Directory**: `./data/`
- **Database File**: `./data/db.sqlite3`
- **Backup**: Simply copy the `data` directory

```bash
# Backup database
cp -r data data-backup-$(date +%Y%m%d)

# Restore database
cp -r data-backup-20231118 data
```

### PostgreSQL

Data persists in Docker volumes:
- **Volume Name**: `postgres_data`
- **Managed by**: Docker

```bash
# Backup database
docker-compose exec db pg_dump -U postgres checkoutdb > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T db psql -U postgres checkoutdb
```

## Admin Access

A default superuser is created automatically:
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`
- **Access URL**: `http://localhost:8000/admin/`

**IMPORTANT**: Change this password in production!

```bash
# Change admin password
docker-compose exec web python manage.py changepassword admin
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs web

# Check all containers
docker-compose ps
```

### Database Issues

```bash
# Reset database (DESTRUCTIVE - deletes all data!)
docker-compose down -v
rm -rf data/
docker-compose up -d

# Check database connection
docker-compose exec web python manage.py dbshell
```

### Permission Issues

```bash
# Fix data directory permissions
sudo chown -R $(whoami):$(whoami) data/
chmod -R 755 data/
```

### Migrations Not Running

```bash
# Manually run migrations
docker-compose exec web python manage.py migrate

# Check migration status
docker-compose exec web python manage.py showmigrations
```

## Production Deployment

### Security Checklist

- [ ] Change `DJANGO_SECRET_KEY` to a random value
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Configure proper `DJANGO_ALLOWED_HOSTS`
- [ ] Change default admin password
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up SSL/TLS termination (nginx/traefik)
- [ ] Configure firewall rules
- [ ] Set up regular database backups
- [ ] Monitor logs and errors
- [ ] Use strong database passwords

### Recommended Docker Compose Production Setup

```yaml
version: '3.8'

services:
  web:
    image: checkoutwebapi:latest
    restart: always
    environment:
      - DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
      - DJANGO_DEBUG=False
      - DJANGO_ALLOWED_HOSTS=${DOMAIN}
      - DB_ENGINE=postgresql
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - backend

  db:
    image: postgres:15-alpine
    restart: always
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/static:ro
    depends_on:
      - web
    networks:
      - backend

volumes:
  postgres_data:

networks:
  backend:
```

## Monitoring

### Health Checks

The application includes health checks:
- **Endpoint**: `http://localhost:8000/`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3

### Viewing Logs

```bash
# All logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Specific service
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100
```

### Resource Usage

```bash
# Container stats
docker stats

# With docker-compose
docker-compose top
```

## Advanced Usage

### Running Django Commands

```bash
# Django shell
docker-compose exec web python manage.py shell

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Run tests
docker-compose exec web python manage.py test
```

### Scaling

```bash
# Scale web service to 3 instances
docker-compose up -d --scale web=3

# Use with a load balancer (nginx/traefik)
```

### Custom Entrypoint

You can override the entrypoint for debugging:

```bash
# Start with bash instead of the application
docker-compose run --rm --entrypoint /bin/bash web
```

## File Structure

```
checkoutWebApiRest/
├── dockerfile                      # Main Docker image definition
├── docker-compose.yml              # SQLite development setup
├── docker-compose.postgres.yml     # PostgreSQL production setup
├── entrypoint.sh                   # Container initialization script
├── .dockerignore                   # Files to exclude from image
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
├── data/                           # SQLite database directory (created at runtime)
│   └── db.sqlite3                  # SQLite database file
├── checkoutWebApiRest/
│   └── settings.py                 # Django settings with env var support
└── DOCKER.md                       # This file
```

## Support

For issues related to Docker setup:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Check file permissions
4. Review this documentation
5. Open an issue on GitHub

## Updates

To update the application:

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose build
docker-compose up -d

# Or with PostgreSQL
docker-compose -f docker-compose.postgres.yml build
docker-compose -f docker-compose.postgres.yml up -d
```
