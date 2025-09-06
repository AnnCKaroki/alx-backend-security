from django.urls import path
from . import views

app_name = 'ip_tracking'

urlpatterns = [
    path('client-info/', views.get_client_info, name='client_info'),
    path('ip-history/', views.get_ip_history, name='ip_history'),
]