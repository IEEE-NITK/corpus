from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
# Create your views here.

def dashboard(request):
    events = Event.objects.all()
    context = {
        "events": events
    }
    return render(request, "events/dashboard.html", context)

def new(request):
    if request.method == "POST":
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, ("New event created!"))
        else:
            print(event_form.errors)
            # messages.error(request, ("Error creating event. Please try again."))
        return redirect("dashboard")
    
    else:
        event_form = EventForm()
    context = {
        "event_form": event_form
    }
    return render(request, "events/new.html", context)

def manage_event(request):
    return render(request, "events/manage_event.html")

def report(request):
    return render(request, "events/report.html")
