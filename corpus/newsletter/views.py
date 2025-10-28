import calendar
import json
from collections import defaultdict
from datetime import date
from datetime import timedelta

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from .forms import EventForm
from .models import Event
from corpus.decorators import ensure_group_membership
from corpus.decorators import module_enabled

from config.models import SIG
from .forms import EventForm
from .models import Event
from corpus.decorators import ensure_group_membership
from corpus.decorators import module_enabled

# Create your views here.
def _daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def calendar_view(request):
    today = timezone.localdate()
    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
        if not (1 <= month <= 12):
            month = today.month
        first_of_month = date(year, month, 1)
    except (ValueError, TypeError):
        year = today.year
        month = today.month
        first_of_month = date(year, month, 1)
    last_of_month = date(year, month, calendar.monthrange(year, month)[1])
    cal = calendar.Calendar(firstweekday=6)  
    raw_all_days = list(cal.itermonthdates(year, month))
    first_day_in_grid = raw_all_days[0]
    last_day_in_grid = raw_all_days[-1]
    events_qs = (
        Event.objects.filter(archive_event=False)
        .filter(Q(start_date__lte=last_day_in_grid) & Q(end_date__gte=first_day_in_grid))
        .prefetch_related("sigs")
        .order_by("start_date", "name")
    )
    day_events = defaultdict(list)
    for e in events_qs:
        start_in_view = max(e.start_date, first_day_in_grid)
        end_in_view = min(e.end_date, last_day_in_grid)
        primary_sig = e.sigs.first()
        for d in _daterange(start_in_view, end_in_view):
            event_data = {
                "id": e.id,
                "name": e.name,
                "page_link": e.page_link,
                "sig_color": primary_sig.color if primary_sig else '#6b7280' 
            }
            event_data["is_first_day_in_view"] = d == start_in_view
            event_data["is_last_day_in_view"] = d == end_in_view
            event_data["is_week_start"] = d.weekday() == 6  # Sunday
            event_data["is_week_end"] = d.weekday() == 5  # Saturday
            
            day_events[d.isoformat()].append(event_data)
    all_cells = []
    for d in raw_all_days:
        iso = d.isoformat() 
        events_for_day = sorted(day_events.get(iso, []), key=lambda x: x["id"])
        all_cells.append(
            {
                "date": d,
                "in_month": (d.month == month),
                "iso": iso,
                "events": events_for_day,
                "count": len(events_for_day),
            }
        )
    prev_month_date = first_of_month - timedelta(days=1)
    next_month_date = last_of_month + timedelta(days=1)
    months = [{"value": i, "name": calendar.month_name[i]} for i in range(1, 13)]
    years = range(today.year - 5, today.year + 6)
    sig_legend = SIG.objects.all().order_by('name').values('name', 'color')
    ctx = {
        "all_cells": all_cells,
        "month_name": calendar.month_name[month],
        "year": year,
        "month": month,
        "prev_year": prev_month_date.year,
        "prev_month": prev_month_date.month,
        "next_year": next_month_date.year,
        "next_month": next_month_date.month,
        "today": today,
        "months": months,
        "years": years,
        "sig_legend": sig_legend,
    }

    return render(request, "newsletter/calendar.html", ctx)


@module_enabled(module_name="newsletter")
def home(request):
    today = timezone.now().date()
    is_admin = request.user.groups.filter(name="newsletter_admin").exists()

    upcoming_or_non_recent = (
        Event.objects.filter(archive_event=False)
        .filter(Q(show_in_recent=False) | Q(start_date__gt=today))
        .order_by("-start_date")
    )

    recent_events = (
        Event.objects.filter(archive_event=False, show_in_recent=True)
        .exclude(thumbnail="")
        .order_by("-start_date")
    )

    return render(
        request,
        "newsletter/home.html",
        {
            "upcoming_events": upcoming_or_non_recent,
            "recent_events": recent_events,
            "is_admin": is_admin,
        },
    )


@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def manage_announcements(request):
    events = Event.objects.all().order_by("-start_date")
    context = {"announcements": events}
    return render(request, "newsletter/manage_announcements.html", context)


@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def new_announcement(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement created successfully")
            return redirect("newsletter_home")
        else:
            messages.error(request, "Failed to create announcement")
            return redirect("newsletter_home")

    form = EventForm()
    context = {"form": form}

    return render(request, "newsletter/new_announcement.html", context)


@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def edit_announcement(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.GET.get("archive") == "true":
        event.archive_event = True
        event.save()
        messages.success(request, "Announcement archived successfully")
        return redirect("newsletter_manage_announcements")

    elif request.GET.get("archive") == "false":
        event.archive_event = False
        event.save()
        messages.success(request, "Announcement unarchived successfully")
        return redirect("newsletter_manage_announcements")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully")
            return redirect("newsletter_manage_announcements")
    else:
        form = EventForm(instance=event)

    return render(
        request,
        "newsletter/edit_announcement.html",
        {"form": form, "announcement": event},
    )


@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def toggle_announcement(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.archive_event = not event.archive_event
    event.save()
    string = "archived" if event.archive_event else "unarchived"
    messages.success(request, f"Announcement {string} successfully")
    return redirect("newsletter_manage_announcements")


@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def delete_announcement(request, pk):
    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        messages.success(request, "Announcement deleted successfully")
        return redirect("newsletter_manage_announcements")
    else:
        messages.warning(request, "Incorrect Request Method. Contact Administrator")
        return redirect("newsletter_manage_announcements")

