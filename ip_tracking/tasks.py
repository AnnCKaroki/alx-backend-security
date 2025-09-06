from celery import shared_task
from django.utils import timezone
from django.db import models
from datetime import timedelta
from .models import IPLog, BlacklistedIP, AnomalyLog


@shared_task
def cleanup_old_ip_logs(days=30):
    """Remove IP logs older than the specified number of days."""
    cutoff_date = timezone.now() - timedelta(days=days)
    deleted_count, _ = IPLog.objects.filter(timestamp__lt=cutoff_date).delete()
    return f"Deleted {deleted_count} IP logs older than {days} days."


@shared_task
def detect_anomalies():
    """Detect anomalous behavior in IP logs."""
    # Example: Detect IPs with high request frequency in the last hour
    cutoff_time = timezone.now() - timedelta(hours=1)
    ip_counts = (
        IPLog.objects.filter(timestamp__gte=cutoff_time)
        .values('ip_address')
        .annotate(request_count=models.Count('id'))
        .filter(request_count__gte=100)  # Threshold for suspicious activity
    )
    
    anomalies_created = 0
    for ip_data in ip_counts:
        AnomalyLog.objects.create(
            ip_address=ip_data['ip_address'],
            description=f"High request frequency: {ip_data['request_count']} requests in the last hour",
            severity='MEDIUM' if ip_data['request_count'] < 200 else 'HIGH'
        )
        anomalies_created += 1
    
    return f"Created {anomalies_created} anomaly logs."


@shared_task
def update_blacklist_status():
    """Update blacklist status for expired entries."""
    now = timezone.now()
    expired_count = BlacklistedIP.objects.filter(
        is_active=True,
        expires_at__lt=now
    ).update(is_active=False)
    
    return f"Updated {expired_count} expired blacklist entries."