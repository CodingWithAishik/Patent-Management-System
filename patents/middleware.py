"""
Rate limiting middleware to prevent abuse from repeated failed attempts.
Simple in-memory cache-based approach suitable for small deployments.
"""
import logging
import time
from collections import defaultdict
from threading import Lock

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    Rate limiting middleware to prevent brute-force and abuse.
    Tracks requests per IP address and applies throttling.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Store request counts per IP: {ip: [(timestamp, count)]}
        self.request_history = defaultdict(list)
        self.lock = Lock()
        # Configuration
        self.window_seconds = 300  # 5-minute window
        self.max_requests = 100  # Allow 100 requests per window
        self.block_seconds = 60  # Block for 1 minute if rate limit exceeded
        self.blocked_ips = {}  # {ip: unblock_time}

    def __call__(self, request):
        client_ip = self.get_client_ip(request)

        # Check if IP is currently blocked
        with self.lock:
            if client_ip in self.blocked_ips:
                if time.time() < self.blocked_ips[client_ip]:
                    logger.warning(f'Rate limit: IP {client_ip} is temporarily blocked')
                    return self.rate_limit_response()
                else:
                    # Unblock expired entry
                    del self.blocked_ips[client_ip]

            # Check request count in current window
            current_time = time.time()
            self.request_history[client_ip] = [
                (ts, count) for ts, count in self.request_history[client_ip]
                if current_time - ts < self.window_seconds
            ]

            request_count = sum(count for _, count in self.request_history[client_ip])
            if request_count >= self.max_requests:
                self.blocked_ips[client_ip] = current_time + self.block_seconds
                logger.warning(
                    f'Rate limit exceeded: IP {client_ip} made {request_count} requests '
                    f'in {self.window_seconds}s. Blocked for {self.block_seconds}s'
                )
                return self.rate_limit_response()

            # Log this request
            self.request_history[client_ip].append((current_time, 1))

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Extract client IP from request, handling proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def rate_limit_response():
        """Return a 429 Too Many Requests response."""
        from django.http import HttpResponse
        return HttpResponse(
            'Too many requests. Please try again later.',
            status=429,
            content_type='text/plain',
        )
