from django.contrib import admin
from .models import IPLog, BlacklistedIP, AnomalyLog


@admin.register(IPLog)
class IPLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'timestamp', 'country', 'city', 'is_blacklisted')
    list_filter = ('is_blacklisted', 'timestamp', 'country')
    search_fields = ('ip_address', 'path', 'country', 'city')
    readonly_fields = ('timestamp',)


@admin.register(BlacklistedIP)
class BlacklistedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason', 'created_at', 'expires_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('ip_address', 'reason')
    readonly_fields = ('created_at',)


@admin.register(AnomalyLog)
class AnomalyLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'severity', 'timestamp', 'is_resolved')
    list_filter = ('severity', 'is_resolved', 'timestamp')
    search_fields = ('ip_address', 'description')
    readonly_fields = ('timestamp',)