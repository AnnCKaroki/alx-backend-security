# IP Tracking Service Startup Guide

This document outlines the steps required to start all services for the IP tracking application.

## Prerequisites

- Python 3.8+ installed
- Redis server installed and running
- All dependencies installed via `pip install -r requirements.txt`

## Starting Services

### 1. Redis Server

Ensure Redis server is running on localhost:6379:

```bash
# On Linux/macOS
redis-server

# On Windows (using Redis for Windows)
start redis-server.exe
```

### 2. Django Application

Start the Django development server:

```bash
python manage.py runserver
```

### 3. Celery Worker

Start the Celery worker for background tasks:

```bash
celery -A alx_backend_security worker -l info
```

### 4. Celery Beat (for scheduled tasks)

Start Celery Beat for periodic tasks:

```bash
celery -A alx_backend_security beat -l info
```

## Verifying Services

1. Django application: Visit http://localhost:8000/admin/ in your browser
2. Redis: Run `redis-cli ping` (should return "PONG")
3. Celery worker: Check the console output for successful startup
4. Celery beat: Check the console output for scheduled tasks

## Common Issues

### Redis Connection Errors

If you encounter Redis connection errors:
- Verify Redis is running with `redis-cli ping`
- Check the Redis connection settings in `settings.py`
- Ensure firewall settings allow connections to Redis port

### Celery Task Failures

If Celery tasks are failing:
- Check the Celery worker logs for specific error messages
- Verify that the task modules are properly imported
- Ensure database migrations are applied

### Rate Limiting Issues

If rate limiting is not working properly:
- Verify Redis cache is configured correctly in settings.py
- Check that middleware is properly ordered in settings.py
- Test with explicit rate limit decorators on views