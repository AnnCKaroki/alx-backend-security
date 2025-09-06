from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from ip_tracking.models import IPLog


class Command(BaseCommand):
    help = 'Generate statistics about IP address activity'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days', type=int, default=7,
            help='Number of days to analyze (default: 7)'
        )
        parser.add_argument(
            '--top', type=int, default=10,
            help='Number of top IPs to show (default: 10)'
        )

    def handle(self, *args, **options):
        days = options['days']
        top_count = options['top']
        
        # Calculate the date range
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Get total request count
        total_requests = IPLog.objects.filter(
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).count()
        
        # Get top IPs by request count
        top_ips = IPLog.objects.filter(
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).values('ip_address').annotate(
            request_count=Count('id')
        ).order_by('-request_count')[:top_count]
        
        # Get top countries
        top_countries = IPLog.objects.filter(
            timestamp__gte=start_date,
            timestamp__lte=end_date,
            country__isnull=False
        ).values('country').annotate(
            request_count=Count('id')
        ).order_by('-request_count')[:top_count]
        
        # Output statistics
        self.stdout.write(self.style.SUCCESS(
            f'IP Statistics for the last {days} days:'
        ))
        self.stdout.write(f'Total requests: {total_requests}')
        
        self.stdout.write('\nTop IPs by request count:')
        for ip_data in top_ips:
            percentage = (ip_data['request_count'] / total_requests) * 100 if total_requests else 0
            self.stdout.write(f"{ip_data['ip_address']}: {ip_data['request_count']} requests ({percentage:.2f}%)")
        
        self.stdout.write('\nTop countries by request count:')
        for country_data in top_countries:
            percentage = (country_data['request_count'] / total_requests) * 100 if total_requests else 0
            self.stdout.write(f"{country_data['country']}: {country_data['request_count']} requests ({percentage:.2f}%)")