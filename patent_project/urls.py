"""
URL configuration for patent_project project.
"""
from django.urls import path, include

urlpatterns = [
    path('', include('patents.urls')),
]
