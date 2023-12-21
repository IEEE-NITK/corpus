from datetime import datetime

from accounts.models import User
from config.models import DATETIME_FORMAT
from config.models import ModuleConfiguration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from embedathon.forms import AnnouncementForm
from embedathon.forms import EmbedathonForm
from embedathon.forms import InviteForm
from embedathon.forms import TeamCreationForm
from embedathon.models import Announcement
from embedathon.models import EmbedathonUser
from embedathon.models import Invite
from embedathon.models import Team

from corpus.decorators import ensure_group_membership
from corpus.decorators import module_enabled


# Create your views here.


def home(request):
    return render(request, "embedathon/home.html")


@login_required
@module_enabled(module_name="embedathon")
def index(request):
    args = {}
    try:
        embedathon_user = EmbedathonUser.objects.get(user=request.user)
        args["embedathon_user"] = embedathon_user
    except EmbedathonUser.DoesNotExist:
        messages.error(request, "Please register for Embedathon first!")
        return redirect("embedathon_register")

    # Check if user is part of a team.
    if embedathon_user.team is not None:
        args["in_team"] = True

        team = embedathon_user.team
        members = EmbedathonUser.objects.filter(team=team)

        args["team"] = team
        args["members"] = members

        if team.team_leader == embedathon_user:
            args["is_leader"] = True
            invites = Invite.objects.filter(inviting_team=team)
            args["invites_from_team"] = invites
            args["invite_form"] = InviteForm()
        else:
            args["is_leader"] = False
    else:
        args["in_team"] = False
        args["is_leader"] = False
        args["team_creation_form"] = TeamCreationForm()
        invites = Invite.objects.filter(invite_email=embedathon_user.user.email)
        args["invites_for_user"] = invites

    config = ModuleConfiguration.objects.get(module_name="embedathon").module_config

    reg_start_datetime, reg_end_datetime = (
        config["reg_start_datetime"],
        config["reg_end_datetime"],
    )

    reg_start_datetime, reg_end_datetime = datetime.strptime(
        reg_start_datetime, DATETIME_FORMAT
    ), datetime.strptime(reg_end_datetime, DATETIME_FORMAT)

    registration_active = (reg_start_datetime <= datetime.now()) and (
        datetime.now() <= reg_end_datetime
    )

    args["registration_active"] = registration_active
    args["announcements"] = Announcement.objects.all().order_by("-pk")

    return render(request, "embedathon/index.html", args)


@login_required
@module_enabled(module_name="embedathon")
def register(request):
    config = ModuleConfiguration.objects.get(module_name="embedathon").module_config

    reg_start_datetime, reg_end_datetime = (
        config["reg_start_datetime"],
        config["reg_end_datetime"],
    )

    reg_start_datetime, reg_end_datetime = datetime.strptime(
        reg_start_datetime, DATETIME_FORMAT
    ), datetime.strptime(reg_end_datetime, DATETIME_FORMAT)

    registration_active = (reg_start_datetime <= datetime.now()) and (
        datetime.now() <= reg_end_datetime
    )

    if not registration_active:
        messages.error(request, "Registration for Embedathon is not active yet.")
        return redirect("index")

    try:
        embedathon_user = EmbedathonUser.objects.get(user=request.user)
        if embedathon_user:
            messages.info(request, "You have already registered!")
            return redirect("embedathon_index")
    except EmbedathonUser.DoesNotExist:
        pass

    if request.method == "POST":
        form = EmbedathonForm(request.POST)
        if form.is_valid():
            embedathon_user = form.save(commit=False)
            embedathon_user.user = request.user
            embedathon_user.save()
            messages.success(request, "Registration successful")
            return redirect("embedathon_index")
    else:
        form = EmbedathonForm()

    args = {"form": form}

    return render(request, "embedathon/register.html", args)


@login_required
@module_enabled(module_name="embedathon")
def create_team(request):
    if request.method == "POST":
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            embedathon_user = EmbedathonUser.objects.get(user=request.user)
            team.team_leader = embedathon_user

            if embedathon_user.from_nitk or embedathon_user.ieee_member:
                team.payment_status = "E"

            team.save()

            embedathon_user.team = team
            embedathon_user.save()

            messages.success(request, "Team created successfully!")
            return redirect("embedathon_index")
    else:
        messages.error(request, "Illegal Request")
        return redirect("embedathon_index")


@login_required
@module_enabled(module_name="embedathon")
def create_invite(request):
    embedathon_user = EmbedathonUser.objects.get(user=request.user)
    if request.method == "POST":
        form = InviteForm(request.POST)
        if form.is_valid():
            if request.user.email == form.cleaned_data["invite_email"]:
                messages.error(request, "You cannot invite yourself!")
                return redirect("embedathon_index")

            try:
                user = User.objects.get(email=form.cleaned_data["invite_email"])
                invited_emb_user = EmbedathonUser.objects.get(user=user)
                if invited_emb_user.team is not None:
                    messages.error(request, "User is already in a team!")
                    return redirect("embedathon_index")
            except (User.DoesNotExist, EmbedathonUser.DoesNotExist):
                pass

            try:
                invite = Invite.objects.get(
                    inviting_team=embedathon_user.team,
                    invite_email=form.cleaned_data["invite_email"],
                )
                messages.error(request, "Invite has already been sent!")
                return redirect("embedathon_index")
            except Invite.DoesNotExist:
                pass

            invite_counts = Invite.objects.filter(
                inviting_team=embedathon_user.team
            ).count()
            team_members = EmbedathonUser.objects.filter(
                team=embedathon_user.team
            ).count()
            config = ModuleConfiguration.objects.get(
                module_name="embedathon"
            ).module_config
            max_count = int(config["max_team_size"])

            if invite_counts >= max_count or team_members >= max_count:
                messages.error(request, "Maximum team member limit reached!")
                return redirect("embedathon_index")

            invite = form.save(commit=False)
            inviting_team = embedathon_user.team
            invite.inviting_team = inviting_team
            invite.save()

            messages.success(request, "Invite sent!")
            return redirect("embedathon_index")
    messages.error(request, "Illegal Request")
    return redirect("embedathon_index")


@login_required
@module_enabled(module_name="embedathon")
def accept_invite(request, pk):
    invite = Invite.objects.get(pk=pk)
    team_members = EmbedathonUser.objects.filter(team=invite.inviting_team).count()
    config = ModuleConfiguration.objects.get(module_name="embedathon").module_config
    max_count = int(config["max_team_size"])

    if team_members >= max_count:
        invite.delete()
        messages.error(request, "Maximum team member limit reached!")
        return redirect("embedathon_index")

    if request.user.email != invite.invite_email:
        messages.error(request, "Illegal request")
        return redirect("embedathon_index")

    embedathon_user = EmbedathonUser.objects.get(user=request.user)
    embedathon_user.team = invite.inviting_team
    embedathon_user.save()

    if embedathon_user.from_nitk or embedathon_user.ieee_member:
        inviting_team = invite.inviting_team
        inviting_team.payment_status = "E"
        inviting_team.save()

    Invite.objects.filter(invite_email=request.user.email).delete()

    messages.success(request, "Invite accepted!")
    return redirect("embedathon_index")


@login_required
@module_enabled(module_name="embedathon")
def delete_invite(request, pk):
    invite = Invite.objects.get(pk=pk)
    invite.delete()

    messages.success(request, "Invite deleted!")
    return redirect("embedathon_index")


@login_required
@ensure_group_membership(group_names=["embedathon_admin"])
def admin(request):
    return render(request, "embedathon/admin.html")


@login_required
@ensure_group_membership(group_names=["embedathon_admin"])
def team_management(request):
    teams = Team.objects.all()
    args = {"teams": teams}
    return render(request, "embedathon/team_management.html", args)


@login_required
@ensure_group_membership(group_names=["embedathon_admin"])
def team_page(request, pk):
    team = Team.objects.get(pk=pk)
    members = EmbedathonUser.objects.filter(team=team)

    args = {"team": team, "members": members}

    return render(request, "embedathon/team_page.html", args)


@login_required
@ensure_group_membership(group_names=["embedathon_admin"])
def mark_payment_complete(request, pk):
    team = Team.objects.get(pk=pk)
    team.payment_status = "P"
    team.save()

    messages.success(request, "Team payment status updated.")
    return redirect("embedathon_admin_team_page", pk=pk)


@login_required
@ensure_group_membership(group_names=["embedathon_admin"])
def user_management(request):
    users = EmbedathonUser.objects.all()

    args = {"users": users}

    return render(request, "embedathon/user_management.html", args)


@login_required
@ensure_group_membership(group_names=["embedathon_admin"])
def announcements_management(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Added announcements.")
            return redirect("embedathon_announcements")
    else:
        form = AnnouncementForm()
        announcements = Announcement.objects.all().order_by("-pk")

        args = {"form": form, "announcements": announcements}

        return render(request, "embedathon/announcements_management.html", args)
