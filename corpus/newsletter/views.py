from django.shortcuts import render
from corpus.decorators import module_enabled
from .models import *
# Create your views here.

@module_enabled(module_name="newsletter")
def home(request):
    announcements = Announcement.objects.filter(archived=False).order_by('-created_at')
    events = Event.objects.filter(archived=False).order_by('-created_at')
    context = {
        'announcements': announcements,
        'events': events
    }
    return render(request, 'newsletter/home.html', context)
