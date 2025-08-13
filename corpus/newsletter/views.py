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


@module_enabled(module_name="newsletter")
def home(request):
    today = timezone.now().date()
    is_admin = request.user.groups.filter(name="newsletter_admin").exists()

    # Events that are either upcoming or not marked for recent display
    upcoming_or_non_recent = (
        Event.objects.filter(archive_event=False)
        .filter(Q(show_in_recent=False) | Q(start_date__gt=today))
        .order_by("-start_date")
    )

    # Events marked for recent display and with a thumbnail
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
