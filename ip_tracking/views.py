from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django_ratelimit.decorators import ratelimit
from django_ip_geolocation.decorators import with_ip_geolocation
from .models import IPLog


@require_GET
@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@with_ip_geolocation
def get_client_info(request):
    """Return client IP and geolocation information."""
    # Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # Get geolocation data if available
    geolocation = getattr(request, 'geolocation', {})
    
    return JsonResponse({
        'ip_address': ip,
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        'geolocation': geolocation
    })


@require_GET
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def get_ip_history(request):
    """Return recent IP logs for the client's IP address."""
    # Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    # Get recent logs for this IP
    logs = IPLog.objects.filter(ip_address=ip).order_by('-timestamp')[:10]
    
    # Format logs for JSON response
    log_data = [{
        'timestamp': log.timestamp.isoformat(),
        'path': log.path,
        'country': log.country,
        'city': log.city
    } for log in logs]
    
    return JsonResponse({
        'ip_address': ip,
        'log_count': len(log_data),
        'logs': log_data
    })