from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from corpus.decorators import ensure_group_membership

# Create your views here.

def dashboard(request):
    is_events_admin = request.user.groups.filter(name="events_admin").exists() if request.user.is_authenticated else False

    events = Event.objects.filter(parent_event=None)
    context = {
        "events": events,
        "admin": is_events_admin,
    }
    return render(request, "events/dashboard.html", context)

@login_required
@ensure_group_membership(group_names=["events_admin"])
def core_dashboard(request):
    events = Event.objects.filter(parent_event=None)
    context = {
        "events": events
    }
    return render(request, "events/core_dashboard.html", context)

@login_required
@ensure_group_membership(group_names=["events_admin"])
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
        return redirect("events_core_dashboard")
    
    else:
        event_form = EventForm()
    context = {
        "event_form": event_form
    }
    return render(request, "events/new.html", context)

@login_required
@ensure_group_membership(group_names=["events_admin"])
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

def show_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    sub_events = Event.objects.filter(parent_event=event).order_by("start_time")
    is_events_admin = request.user.groups.filter(name="events_admin").exists() if request.user.is_authenticated else False
    context = {
        "event": event,
        "sub_events": sub_events,
        "is_events_admin": is_events_admin,
    }
    return render(request, "events/show_event.html", context)

@login_required
@ensure_group_membership(group_names=["events_admin"])
def delete_event(request, pk):
    event = get_object_or_404(Event, id=pk)
    event.delete()
    messages.success(request, ("Event deleted successfully!"))
    return redirect("events_core_dashboard")

def report(request):
    return render(request, "events/report.html")
