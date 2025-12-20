import calendar
import json
from collections import defaultdict
from datetime import date
from datetime import timedelta

from config.models import SIG
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
        Event.objects.filter(
            Q(start_date__lte=last_day_in_grid) & Q(end_date__gte=first_day_in_grid)
        )
        .prefetch_related("sigs")
        .order_by("start_date", "name")
    )
    day_events = defaultdict(list)
    for e in events_qs:
        start_in_view = max(e.start_date, first_day_in_grid)
        end_in_view = min(e.end_date, last_day_in_grid)
        primary_sig = e.sigs.first()
        sig_names = [sig.name for sig in e.sigs.all()]
        sigs_data = [{"name": sig.name, "color": sig.color} for sig in e.sigs.all()]
        sigs_json = json.dumps(sigs_data)
        if len(sig_names) >= 2:
            final_color = "#000080"
        else:
            final_color = primary_sig.color if primary_sig else "#6b7280"
        for d in _daterange(start_in_view, end_in_view):
            event_data = {
                "id": e.id,
                "name": e.name,
                "description": e.description or "",
                "page_link": e.page_link,
                "sig_color": final_color,
                "sigs_json": sigs_json,
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
    sig_legend = SIG.objects.all().order_by("name").values("name", "color")
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
def archived_events_view(request):
    events_qs = Event.objects.filter(archive_event=True).order_by("-start_date") 
    is_admin = request.user.groups.filter(name="newsletter_admin").exists()
    available_years = (
        Event.objects.filter(archive_event=True)
        .values_list("start_date__year", flat=True)
        .distinct()
        .order_by("-start_date__year")
    )
    all_sigs = SIG.objects.all().order_by("name")
    selected_year = request.GET.get("year")
    selected_sig_id = request.GET.get("sig")
    if selected_year:
        try:
            year = int(selected_year)
            events_qs = events_qs.filter(start_date__year=year) 
        except ValueError:
            selected_year = None
    if selected_sig_id:
        try:
            sig_id = int(selected_sig_id)
            events_qs = events_qs.filter(sigs__id=sig_id)
        except ValueError:
            selected_sig_id = None
    context = {
        "events": events_qs.prefetch_related("sigs"),
        "available_years": available_years,
        "all_sigs": all_sigs,
        "selected_year": selected_year,
        "selected_sig_id": selected_sig_id,
        "is_admin" : is_admin,
    }
    return render(request, "newsletter/archived_events.html", context)

@module_enabled(module_name="newsletter")
def archived_event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.prefetch_related('sigs'), 
        pk=pk, 
        archive_event=True
    )

    context = {
        "event": event,
    }
    
    return render(request, "newsletter/archived_event_detail.html", context)

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
            return redirect(request.GET.get("next", "newsletter_manage_announcements"))

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
    return redirect(
        request.GET.get("next")
        or request.POST.get("next")
        or "newsletter_manage_announcements"
    )

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
