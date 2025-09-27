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

# Create your views here.


SIG_PALETTE = [
    "#2563eb",
    "#16a34a",
    "#dc2626",
    "#7c3aed",
]
NO_SIG_COLOR = "#6b7280"


def _sig_color(sig_id: int) -> str:
    return SIG_PALETTE[(sig_id - 1) % len(SIG_PALETTE)]


def _daterange(d0: date, d1: date):
    """Yield all dates from d0 to d1 inclusive."""
    delta = (d1 - d0).days
    for i in range(delta + 1):
        yield d0 + timedelta(days=i)


def _event_payload(e) -> dict:
    sigs = list(e.sigs.all())
    if sigs:
        sig_list = [
            {"id": s.id, "name": s.name, "color": _sig_color(s.id)} for s in sigs
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


def _unique_sig_colors(events_for_day):
    seen = set()
    colors = []
    for evt in events_for_day:
        for s in evt["sigs"]:
            c = s["color"]
            if c not in seen:
                seen.add(c)
                colors.append(c)
    return colors[:6]


def calendar_view(request):
    today = timezone.localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

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
        duration = (e.end_date - e.start_date).days + 1
        if duration > 5:
            if first_of_month <= e.start_date <= last_of_month:
                key = e.start_date.isoformat()
                day_events[key].append(_event_payload(e))
        else:
            start = max(e.start_date, first_of_month)
            end = min(e.end_date, last_of_month)
            for d in _daterange(start, end):
                day_events[d.isoformat()].append(_event_payload(e))

    cal = calendar.Calendar(firstweekday=6)
    raw_all_days = list(cal.itermonthdates(year, month))

    all_cells = []
    for d in raw_all_days:
        iso = d.isoformat()
        events_for_day = day_events.get(iso, [])
        sig_colors = _unique_sig_colors(events_for_day)
        all_cells.append(
            {
                "date": d,
                "in_month": (d.month == month),
                "iso": iso,
                "events": events_for_day,
                "sig_colors": sig_colors,
                "count": len(events_for_day),
            }
        )

    day_events_json = json.dumps(day_events)

    prev_year, prev_month = (year, month - 1) if month > 1 else (year - 1, 12)
    next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)

    ctx = {
        "all_cells": all_cells,
        "month_name": calendar.month_name[month],
        "year": year,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "today": today,
        "day_events_json": day_events_json,
        "no_sig_color": NO_SIG_COLOR,
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
