from django.shortcuts import render, redirect, get_object_or_404
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

def core_dashboard(request):
    events = Event.objects.all()
    context = {
        "events": events
    }
    return render(request, "events/core_dashboard.html", context)


def new(request):
    if request.method == "POST":
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            instance = event_form.save(commit=False)
            instance.save()
            event_form.save_m2m()
            messages.success(request, ("New event created!"))
        else:
            print(event_form.errors)
            messages.error(request, ("Error creating event. Please try again."))
        return redirect("dashboard")
    
    else:
        event_form = EventForm()
    context = {
        "event_form": event_form
    }
    return render(request, "events/new.html", context)

def manage_event(request, pk):
    event = get_object_or_404(Event, id=pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, ("Event updated successfully!"))
        else:
            print(form.errors)
            messages.error(request, ("Error updating event. Please try again."))
        return redirect("events_core_dashboard")
    else:
        form = EventForm(instance=event)
    context = {
        "event": event,
        "form": form,
    }
    return render(request, "events/manage_event.html", context)

def delete_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    event.delete()
    messages.success(request, ("Event deleted successfully!"))
    return redirect("events_core_dashboard")

def report(request):
    return render(request, "events/report.html")
