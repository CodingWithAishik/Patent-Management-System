"""
Health check endpoints for monitoring app status.
"""
from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError
import logging

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Basic health check endpoint.
    Returns 200 if app is running, 500 if database is unreachable.
    Used by monitoring and load balancers.
    """
    try:
        # Test database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'message': 'Patent Management System is operational',
        }, status=200)
    
    except OperationalError as e:
        logger.error(f'Health check failed: Database error: {e}')
        return JsonResponse({
            'status': 'unhealthy',
            'message': 'Database connection failed',
            'detail': str(e),
        }, status=500)
    
    except Exception as e:
        logger.error(f'Health check failed: Unexpected error: {e}')
        return JsonResponse({
            'status': 'unhealthy',
            'message': 'Unexpected error',
            'detail': str(e),
        }, status=500)


def readiness_check(request):
    """
    Readiness check for deployment pipelines.
    Verifies the app is ready to handle traffic.
    """
    return JsonResponse({
        'status': 'ready',
        'service': 'Patent Management System',
    }, status=200)
