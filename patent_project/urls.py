"""
URL configuration for patent_project project.
"""
from django.urls import path, include
from patents.health_check import health_check, readiness_check

urlpatterns = [
    # Health check endpoints for monitoring/load balancers
    path('health/', health_check, name='health_check'),
    path('ready/', readiness_check, name='readiness_check'),
    
    # Main app URLs
    path('', include('patents.urls')),
]
