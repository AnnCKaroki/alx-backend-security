from django.utils import timezone
from django.http import HttpResponseForbidden
from django_ip_geolocation.decorators import with_ip_geolocation
from django_ratelimit.exceptions import Ratelimited
from .models import IPLog, BlacklistedIP


class IPTrackingMiddleware:
    """Middleware for tracking IP addresses and logging them."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get IP address
        ip_address = self.get_client_ip(request)
        
        # Check if IP is blacklisted
        if self.is_blacklisted(ip_address):
            return HttpResponseForbidden("Your IP address has been blacklisted.")
        
        # Process the request
        response = self.get_response(request)
        
        # Log the IP after processing (to include any geolocation data added by django_ip_geolocation)
        self.log_ip(request, ip_address)
        
        return response
    
    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_blacklisted(self, ip_address):
        """Check if an IP address is blacklisted."""
        blacklisted = BlacklistedIP.objects.filter(
            ip_address=ip_address,
            is_active=True
        )
        
        # Check for expired blacklists and update them
        for item in blacklisted:
            if item.expires_at and item.expires_at < timezone.now():
                item.is_active = False
                item.save()
        
        # Return True if there are any active blacklisted entries
        return blacklisted.filter(is_active=True).exists()
    
    def log_ip(self, request, ip_address):
        """Log the IP address and related information."""
        # Get geolocation data if available
        geolocation = getattr(request, 'geolocation', {})
        
        # Create log entry
        IPLog.objects.create(
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            path=request.path,
            is_blacklisted=False,
            country=geolocation.get('country_name'),
            city=geolocation.get('city'),
            region=geolocation.get('region'),
            latitude=geolocation.get('latitude'),
            longitude=geolocation.get('longitude')
        )


class RateLimitExceptionMiddleware:
    """Middleware for handling rate limit exceptions."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        if isinstance(exception, Ratelimited):
            return HttpResponseForbidden(
                "Rate limit exceeded. Please try again later.",
                content_type="text/plain"
            )
        return None