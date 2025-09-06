from django.db import models


class IPLog(models.Model):
    """Model for logging IP addresses and related information."""
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_blacklisted = models.BooleanField(default=False)
    
    # Geolocation fields
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'IP Log'
        verbose_name_plural = 'IP Logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"


class BlacklistedIP(models.Model):
    """Model for storing blacklisted IP addresses."""
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Blacklisted IP'
        verbose_name_plural = 'Blacklisted IPs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.ip_address} - {self.reason}"


class AnomalyLog(models.Model):
    """Model for logging anomalous behavior."""
    ip_address = models.GenericIPAddressField()
    description = models.TextField()
    severity = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
            ('CRITICAL', 'Critical'),
        ],
        default='MEDIUM'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Anomaly Log'
        verbose_name_plural = 'Anomaly Logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.ip_address} - {self.severity} - {self.timestamp}"