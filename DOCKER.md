# Docker Setup for Notes App (Python/Flask)

This guide explains how to run the Notes App using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)

## Quick Start

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/mgrandusky/notes-app-python.git
   cd notes-app-python
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Build and start the containers**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   - Open your browser to http://localhost:5000

## Docker Commands

### Start the application
```bash
docker-compose up -d
```

### Stop the application
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f web
```

### Initialize database (if needed)
The database tables are automatically created on first run. To manually trigger:
```bash
docker-compose exec web flask shell
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

### Access the Flask shell
```bash
docker-compose exec web flask shell
```

### Rebuild containers (after code changes)
```bash
docker-compose up -d --build
```

## Environment Variables

Key environment variables (set in `.env` file):

- `SECRET_KEY` - Flask secret key for sessions
- `DATABASE_URL` - PostgreSQL connection string (automatically set in docker-compose)
- `MAIL_SERVER` - SMTP server for email
- `MAIL_USERNAME` - Email username
- `MAIL_PASSWORD` - Email password
- `GOOGLE_CLIENT_ID` - Google OAuth client ID (optional)
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret (optional)
- `GITHUB_CLIENT_ID` - GitHub OAuth client ID (optional)
- `GITHUB_CLIENT_SECRET` - GitHub OAuth client secret (optional)

## Development Mode

For development with live reloading:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

Create a `docker-compose.dev.yml`:
```yaml
version: '3.8'

services:
  web:
    command: flask run --host=0.0.0.0 --port=5000 --reload
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
```

## Production Deployment

For production:

1. **Change default credentials**: Update database credentials in `docker-compose.yml` or use `docker-compose.override.yml`
2. Set strong `SECRET_KEY` in `.env` (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
3. Configure proper email settings
4. Set up OAuth credentials (if using)
5. Use a managed PostgreSQL database (recommended)
6. Set up a reverse proxy (nginx) in front of the Flask app
7. Enable HTTPS
8. Remove or restrict volume mounts to prevent exposing sensitive files

**Security Note**: The default `docker-compose.yml` uses hard-coded database credentials suitable for development only. For production, create a `docker-compose.override.yml` with secure credentials or use environment variables.

## Troubleshooting

### Database connection errors
```bash
docker-compose down -v
docker-compose up -d
```

### Permission issues
```bash
sudo chown -R $USER:$USER .
```

### View container status
```bash
docker-compose ps
```

## Volume Management

Data is persisted in Docker volumes:
- `postgres_data` - PostgreSQL database data

To backup the database:
```bash
docker-compose exec postgres pg_dump -U user notesapp > backup.sql
```

To restore:
```bash
docker-compose exec -T postgres psql -U user notesapp < backup.sql
```
