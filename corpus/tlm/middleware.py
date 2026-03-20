from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from zoneinfo import ZoneInfo

class TLMLaunchGateMiddleware:
    LAUNCH_URL_PREFIX = '/tlm/landing/bro'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz = ZoneInfo('Asia/Kolkata')
        launch = datetime(2026, 3, 20, 18, 0, 0, tzinfo=tz)

        if request.path.startswith(self.LAUNCH_URL_PREFIX):
            if timezone.now() < launch:
                    return render(request, 'tlm/403.html', status=403)

        return self.get_response(request)