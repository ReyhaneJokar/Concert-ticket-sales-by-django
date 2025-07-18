import time
import logging

from django.utils.deprecation import MiddlewareMixin

request_logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        # processing time
        elapsed = (time.time() - getattr(request, '_start_time', time.time())) * 1000
        data = {
            'method': request.method,
            'path':   request.get_full_path(),
            'status': response.status_code,
            'duration_ms': round(elapsed, 2),
            'remote_addr': request.META.get('REMOTE_ADDR'),
        }
        request_logger.info(f"{data}")
        return response
