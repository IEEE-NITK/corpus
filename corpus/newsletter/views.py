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
SIG_PALETTE = [
    "#7c3aed", #intersig
    "#fba418", #compsoc
    "#59f3e9", #diode
    "#cb0011", #piston
]
NO_SIG_COLOR = "#6b7280"


def get_sig_color(sig_id: int) -> str:
    """Returns a color for a given SIG ID based on the palette."""
    if not sig_id:
        return NO_SIG_COLOR
    return SIG_PALETTE[(sig_id - 1) % len(SIG_PALETTE)]


def _daterange(d0: date, d1: date):
    """Yield all dates from d0 to d1 inclusive."""
    delta = (d1 - d0).days
    for i in range(delta + 1):
        yield d0 + timedelta(days=i)


def _event_payload(e) -> dict:
    sigs = list(e.sigs.all())
    if sigs:
        # Use the imported get_sig_color function
        sig_list = [
            {"id": s.id, "name": s.name, "color": get_sig_color(s.id)} for s in sigs
        ]
    else:
        sig_list = [{"id": 0, "name": "No SIG", "color": NO_SIG_COLOR}]
    return {
        "id": e.id,
        "name": e.name,
        "page_link": e.page_link or "",
        "start_date": e.start_date.isoformat(),
        "end_date": e.end_date.isoformat(),
        "sigs": sig_list,
    }


def calendar_view(request):
    today = timezone.localdate()
    try:
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))
        # Basic validation for year and month
        if not (1 <= month <= 12):
            month = today.month
        first_of_month = date(year, month, 1)
    except (ValueError, TypeError):
        year = today.year
        month = today.month
        first_of_month = date(year, month, 1)

    last_of_month = date(year, month, calendar.monthrange(year, month)[1])

    events_qs = (
        Event.objects.filter(archive_event=False)
        .filter(Q(start_date__lte=last_of_month) & Q(end_date__gte=first_of_month))
        .prefetch_related("sigs")
        .order_by("start_date", "name")
    )

    day_events = defaultdict(list)

    for e in events_qs:
        start_in_view = max(e.start_date, first_of_month)
        end_in_view = min(e.end_date, last_of_month)

        for d in _daterange(start_in_view, end_in_view):
            event_data = _event_payload(e)
            event_data["is_first_day_in_view"] = d == start_in_view
            event_data["is_last_day_in_view"] = d == end_in_view
            # weekday(): Monday is 0 and Sunday is 6
            event_data["is_week_start"] = d.weekday() == 6  # Sunday
            event_data["is_week_end"] = d.weekday() == 5  # Saturday
            day_events[d.isoformat()].append(event_data)

    cal = calendar.Calendar(firstweekday=6)  # Sunday is the first day of the week
    raw_all_days = list(cal.itermonthdates(year, month))

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

    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    months = [{"value": i, "name": calendar.month_name[i]} for i in range(1, 13)]
    years = range(today.year - 5, today.year + 6)
    
    
    all_sigs = SIG.objects.all().order_by('id')
    sig_legend = [
        {"name": sig.name, "color": get_sig_color(sig.id)}
        for sig in all_sigs
    ]
    
    ctx = {
        "all_cells": all_cells,
        "month_name": calendar.month_name[month],
        "year": year,
        "month": month,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "today": today,
        "no_sig_color": NO_SIG_COLOR,
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

