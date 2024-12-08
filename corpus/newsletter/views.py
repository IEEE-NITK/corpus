from django.shortcuts import render
from .models import NewsPost
from events.models import Event
from datetime import datetime

# Create your views here.

def home(request):
    upcoming_events = Event.objects.filter(start_time__gte=datetime.now())
    upcoming_events_posts = NewsPost.objects.filter(event__in=upcoming_events)
    posts = NewsPost.objects.all().order_by('-date')[:5]
    completed_events = Event.objects.filter(end_time__lte=datetime.now())
    completed_events_posts = NewsPost.objects.filter(event__in=completed_events)
    context = {
        'upcoming_events_posts': upcoming_events_posts,
        'completed_events_posts': completed_events_posts,
        'posts': posts
    }
    return render(request, "newsletter/home.html", context)
