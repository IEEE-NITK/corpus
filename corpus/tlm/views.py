from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from zoneinfo import ZoneInfo

def home(request):
    return render(request, "tlm/home.html")

def landing(request):
    return render(request, 'tlm/landing.html')