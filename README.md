# ALX Backend Security

A Django application implementing various security features including IP logging, blacklisting, geolocation, rate limiting, and anomaly detection.

## Project Setup

### Prerequisites

- Python 3.x
- Redis server running on localhost:6379

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd alx-backend-security
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install django-ip-geolocation django-ratelimit celery redis django-celery-beat
   ```

4. Apply database migrations:
   ```
   python manage.py makemigrations ip_tracking
   python manage.py migrate
   ```

5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```

### Running the Application

You need to run multiple services in separate terminals:

1. Start the Redis server (if not already running):
   ```
   redis-server
   ```

2. Start the Django development server:
   ```
   python manage.py runserver
   ```

3. Start the Celery worker:
   ```
   celery -A alx_backend_security worker --loglevel=info
   ```

4. Start the Celery Beat scheduler:
   ```
   celery -A alx_backend_security beat --loglevel=info
   ```

## Features

### IP Tracking

- Logs all IP addresses accessing the application
- Stores geolocation data for each IP
- Provides admin interface to view and manage IP logs

### IP Blacklisting

- Block specific IP addresses from accessing the application
- Set expiration dates for blacklisted IPs
- Command-line interface for managing blacklisted IPs

### Rate Limiting

- Limits the number of requests per IP address
- Configurable rate limits for different views
- Custom error responses for rate-limited requests

### Anomaly Detection

- Identifies suspicious behavior patterns
- Logs anomalies with severity levels
- Scheduled tasks for automated detection

## API Endpoints

- `/ip/client-info/` - Returns client IP and geolocation information
- `/ip/ip-history/` - Returns recent access history for the client's IP

## Management Commands

- `python manage.py blacklist_ip <ip_address> <reason> [--days DAYS]` - Blacklist an IP address
- `python manage.py ip_stats [--days DAYS] [--top TOP]` - Generate IP statistics

## Trade-offs and Security Considerations

- **Performance Impact**: IP logging and geolocation lookups add overhead to each request. Consider caching geolocation data for frequently seen IPs.
- **Privacy Implications**: Collecting and storing IP addresses and geolocation data has privacy implications. Ensure compliance with relevant regulations like GDPR.
- **False Positives**: Rate limiting and anomaly detection may occasionally block legitimate users. Consider implementing mechanisms for users to request temporary access.
- **Database Growth**: IP logs can grow quickly on high-traffic sites. Implement regular cleanup tasks to manage database size.