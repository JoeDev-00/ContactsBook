import sys
import traceback
from django.conf import settings

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if settings.DEBUG:
            print(''.join(traceback.format_exception(*sys.exc_info())))
        return None
