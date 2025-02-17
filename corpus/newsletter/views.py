from django.shortcuts import get_object_or_404, render, redirect
from corpus.decorators import ensure_group_membership, module_enabled
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.

@module_enabled(module_name="newsletter")
def home(request):
    announcements = Announcement.objects.filter(archived=False).order_by('-created_at')
    events = Event.objects.filter(archived=False).order_by('-created_at')
    is_admin = request.user.groups.filter(name="newsletter_admin").exists()
    context = {
        'announcements': announcements,
        'events': events,
        'is_admin': is_admin,
    }
    return render(request, 'newsletter/home.html', context)

@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def manage_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    context = {
        'announcements': announcements
    }
    return render(request, 'newsletter/manage_announcements.html', context)

@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def new_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save()
            messages.success(request, "Announcement created successfully")
            return redirect('newsletter_home')
        else:
            messages.error(request, "Failed to create announcement")
            return redirect('newsletter_home')
        
    form = AnnouncementForm()
    context = {
        "form": form
    }

    return render(request, 'newsletter/new_announcement.html', context)

@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement updated successfully")
            return redirect('newsletter_manage_announcements')
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'newsletter/edit_announcement.html', {'form': form, 'announcement': announcement})

@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def toggle_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.archived = not announcement.archived
    announcement.save()
    string = "archived" if announcement.archived else "unarchived"
    messages.success(request, f"Announcement {string} successfully")
    return redirect('newsletter_manage_announcements')

@module_enabled(module_name="newsletter")
@ensure_group_membership(group_names=["newsletter_admin"])
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    messages.success(request, "Announcement deleted successfully")
    return redirect('newsletter_manage_announcements')


    