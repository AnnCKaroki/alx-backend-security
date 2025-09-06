from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import timedelta
from ip_tracking.models import BlacklistedIP


class Command(BaseCommand):
    help = 'Blacklist an IP address with an optional expiration time'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='IP address to blacklist')
        parser.add_argument('reason', type=str, help='Reason for blacklisting')
        parser.add_argument(
            '--days', type=int, default=None,
            help='Number of days the IP should be blacklisted (default: permanent)'
        )

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options['reason']
        days = options['days']
        
        # Calculate expiration date if days are provided
        expires_at = None
        if days is not None:
            expires_at = timezone.now() + timedelta(days=days)
        
        # Create or update blacklist entry
        blacklist, created = BlacklistedIP.objects.update_or_create(
            ip_address=ip_address,
            defaults={
                'reason': reason,
                'expires_at': expires_at,
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully blacklisted IP {ip_address}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Updated blacklist entry for IP {ip_address}')
            )
        
        if expires_at:
            self.stdout.write(f'Blacklist will expire on {expires_at}')