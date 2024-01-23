from datetime import datetime

from accounts.models import User
from config.models import DATETIME_FORMAT
from config.models import ModuleConfiguration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from electrika.forms import AnnouncementForm
from electrika.forms import ElectrikaForm
from electrika.forms import InviteForm
from electrika.forms import TeamCreationForm
from electrika.models import Announcement
from electrika.models import ElectrikaUser
from electrika.models import Invite
from electrika.models import Team

from corpus.decorators import ensure_group_membership
from corpus.decorators import module_enabled
from corpus.utils import send_email


# Create your views here.
@module_enabled(module_name="electrika")
def home(request):
    args = {}

    # Checking if user is Electrika_admin group member
    if request.user.groups.filter(name="electrika_admin").exists():
        args = {"admin": True}
    config = ModuleConfiguration.objects.get(module_name="electrika").module_config

    try:
        if request.user.is_authenticated:
            electrika_user = ElectrikaUser.objects.get(user=request.user)
            args["registered"] = True
            args["electrika_user"] = electrika_user
    except ElectrikaUser.DoesNotExist:
        args["registered"] = False

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

    registration_done = reg_end_datetime < datetime.now()

    args["session_link"] = config["session-link"]

    args["registration_active"] = registration_active
    args["registration_done"] = registration_done

    return render(
        request,
        "electrika/home.html",
        args,
    )


@login_required
@module_enabled(module_name="electrika")
def index(request):
    args = {}
    try:
        electrika_user = ElectrikaUser.objects.get(user=request.user)
        args["electrika_user"] = electrika_user
    except ElectrikaUser.DoesNotExist:
        messages.error(request, "Please register for Electrika first!")
        return redirect("electrika_register")

    if electrika_user.team is not None:
        args["in_team"] = True

        args["team_creation_form"] = TeamCreationForm(instance=electrika_user.team)

        team = electrika_user.team
        members = ElectrikaUser.objects.filter(team=team)
        team_count = members.count()

        config = ModuleConfiguration.objects.get(module_name="electrika").module_config

        max_count = int(config["max_team_size"])

        args["max_count"] = max_count

        if team_count >= max_count:
            args["team_full"] = True
        if team.team_leader == electrika_user:
            args["is_leader"] = True
            invites = Invite.objects.filter(inviting_team=team)
            args["invites_from_team"] = invites
            args["invite_form"] = InviteForm()
        else:
            args["is_leader"] = False

        args["team_count"] = team_count

        args["team"] = team
        args["members"] = members

    else:
        args["in_team"] = False
        args["is_leader"] = False
        args["team_creation_form"] = TeamCreationForm()
        invites = Invite.objects.filter(invite_email=electrika_user.user.email)
        args["invites_for_user"] = invites

    config = ModuleConfiguration.objects.get(module_name="electrika").module_config

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

    if electrika_user.team is not None:
        announcements = Announcement.objects.filter(announcement_type__in=["A", "T"])
    else:
        announcements = Announcement.objects.filter(announcement_type__in=["A", "N"])

    announcements = announcements.order_by("-date_created")

    args["announcements"] = announcements

    return render(request, "electrika/index.html", args)


@login_required
@module_enabled(module_name="electrika")
def register(request):
    config = ModuleConfiguration.objects.get(module_name="electrika").module_config

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
        messages.error(request, "Registration for Electrika is not active yet!")
        return redirect("index")

    try:
        electrika_user = ElectrikaUser.objects.get(user=request.user)
        messages.error(request, "You have already registered for Electrika!")
        return redirect("electrika_index")
    except ElectrikaUser.DoesNotExist:
        pass

    if request.method == "POST":
        form = ElectrikaForm(request.POST)
        if form.is_valid():
            electrika_user = form.save(commit=False)
            electrika_user.user = request.user
            electrika_user.save()
            messages.success(request, "Successfully registered for Electrika!")
            return redirect("electrika_index")
        else:
            messages.error(request, "Please correct the errors before registering!")

    else:
        form = ElectrikaForm()

    args = {"form": form}
    return render(request, "electrika/register.html", args)


@login_required
@module_enabled(module_name="electrika")
def create_team(request):
    if request.method == "POST":
        form = TeamCreationForm(request.POST)
        electrika_user = ElectrikaUser.objects.get(user=request.user)
        if electrika_user.team is not None:
            if form.is_valid():
                team = electrika_user.team
                team.team_name = form.cleaned_data["team_name"]
                team.save()
                messages.success(request, "Successfully updated team name!")
                return redirect("electrika_index")
        else:
            if form.is_valid():
                team = form.save(commit=False)
                electrika_user = ElectrikaUser.objects.get(user=request.user)
                team.team_leader = electrika_user

                team.save()
                electrika_user.team = team
                electrika_user.to_be_teamed_up = False
                electrika_user.save()
                messages.success(request, "Successfully created team!")
                return redirect("electrika_index")
    else:
        messages.error(request, "Please correct the errors before creating team!")
        return redirect("electrika_index")


@login_required
@module_enabled(module_name="electrika")
def create_invite(request):
    electrika_user = ElectrikaUser.objects.get(user=request.user)
    if request.method == "POST":
        form = InviteForm(request.POST)
        if form.is_valid():
            if request.user.email == form.cleaned_data["invite_email"]:
                messages.error(request, "You cannot invite yourself!")
                return redirect("electrika_index")

            try:
                user = User.objects.get(email=form.cleaned_data["invite_email"])
                invited_imp_user = ElectrikaUser.objects.get(user=user)
                if invited_imp_user.team is not None:
                    messages.error(request, "User is already in a team!")
                    return redirect("electrika_index")
            except (User.DoesNotExist, ElectrikaUser.DoesNotExist):
                pass

            try:
                invite = Invite.objects.get(
                    inviting_team=electrika_user.team,
                    invite_email=form.cleaned_data["invite_email"],
                )
                messages.error(request, "Invite has already been sent!")
                return redirect("electrika_index")
            except Invite.DoesNotExist:
                pass

            invite_counts = Invite.objects.filter(
                inviting_team=electrika_user.team
            ).count()

            team_members = ElectrikaUser.objects.filter(
                team=electrika_user.team
            ).count()

            config = ModuleConfiguration.objects.get(
                module_name="electrika"
            ).module_config
            max_count = int(config["max_team_size"])

            if invite_counts >= max_count or team_members >= max_count:
                messages.error(request, "Maximum team member limit reached!")
                return redirect("electrika_index")

            invite = form.save(commit=False)
            inviting_team = electrika_user.team
            invite.inviting_team = inviting_team
            invite.save()

            messages.success(request, "Invite sent!")
            return redirect("electrika_index")
    messages.error(request, "Illegal Request")
    return redirect("electrika_index")


@login_required
@module_enabled(module_name="electrika")
def accept_invite(request, pk):
    invite = Invite.objects.get(pk=pk)
    team_members = ElectrikaUser.objects.filter(team=invite.inviting_team).count()
    config = ModuleConfiguration.objects.get(module_name="electrika").module_config
    max_count = int(config["max_team_size"])

    if team_members >= max_count:
        invite.delete()
        messages.error(request, "Maximum team member limit reached!")
        return redirect("electrika_index")

    if request.user.email != invite.invite_email:
        messages.error(request, "Illegal request")
        return redirect("electrika_index")

    electrika_user = ElectrikaUser.objects.get(user=request.user)
    electrika_user.team = invite.inviting_team
    electrika_user.to_be_teamed_up = False
    electrika_user.save()

    Invite.objects.filter(invite_email=request.user.email).delete()

    messages.success(request, "Invite accepted!")
    return redirect("electrika_index")


@login_required
@module_enabled(module_name="electrika")
def delete_invite(request, pk):
    invite = Invite.objects.get(pk=pk)
    invite.delete()

    messages.success(request, "Invite deleted!")
    return redirect("electrika_index")


@login_required
@module_enabled(module_name="electrika")
def opt_in(request):
    electrika_user = ElectrikaUser.objects.get(user=request.user)
    electrika_user.to_be_teamed_up = True
    electrika_user.save()
    messages.success(request, "Successfully opted in for team formation!")
    return redirect("electrika_index")


@login_required
@module_enabled(module_name="electrika")
def opt_out(request):
    electrika_user = ElectrikaUser.objects.get(user=request.user)
    electrika_user.to_be_teamed_up = False
    electrika_user.save()
    messages.success(request, "Successfully opted out for team formation!")
    return redirect("electrika_index")


@login_required
@ensure_group_membership(group_names=["electrika_admin"])
def admin(request):
    return render(request, "electrika/admin/admin.html", {})


@login_required
@ensure_group_membership(group_names=["electrika_admin"])
def team_management(request):
    args = {}
    args["teams"] = Team.objects.all()
    return render(request, "electrika/admin/teams.html", args)


@login_required
@ensure_group_membership(group_names=["electrika_admin"])
def team_page(request, pk):
    args = {}
    team = Team.objects.get(pk=pk)
    args["team"] = team
    args["members"] = ElectrikaUser.objects.filter(team=team)
    return render(request, "electrika/admin/team_page.html", args)


@login_required
@ensure_group_membership(group_names=["electrika_admin"])
def create_team_admin(request):
    import random

    random.seed(datetime.now().second)
    electrika_users = ElectrikaUser.objects.filter(team=None, to_be_teamed_up=True)
    TEAM_NAMES = [
        "Iconoclasts",
        "Nihilists",
        "Antagonists",
        "Whiz Kids",
        "The Geek Squad",
        "Net Surfers",
        "The Informants",
        "Black Hat Hackers",
        "Brainiacs",
        "Quizzical Education",
        "Phone a Friend",
        "Witches and Quizards",
        "The Quizzy Bees",
        "Wallflowers",
        "Smart Simpson",
        "Cheat Sheet",
        "You Cheated Off Us in High School",
        "Brainstormers",
    ]

    num_users = electrika_users.count()
    num_teams = num_users // 4

    electrika_users = list(electrika_users)

    if num_users == 0:
        messages.error(request, "Not enough users to create teams!")
        return redirect("electrika_admin_teams")

    try:
        with transaction.atomic():
            for i in range(num_teams):
                team_name = TEAM_NAMES[random.randint(0, len(TEAM_NAMES) - 1)]
                team_leader_index = i * 4
                team_leader = electrika_users[team_leader_index]
                team = Team(team_name=team_name, team_leader=team_leader)
                team.save()
                for j in range(4):
                    index = i * 4 + j
                    if index >= len(electrika_users):
                        break
                    user = electrika_users[index]
                    user.team = team
                    user.to_be_teamed_up = False
                    user.save()

            if num_users % 4 != 0:
                team_name = TEAM_NAMES[random.randint(0, len(TEAM_NAMES) - 1)]
                team_leader_index = num_teams * 4
                team = Team(
                    team_name=team_name, team_leader=electrika_users[team_leader_index]
                )
                team.save()
                for j in range(num_users % 4):
                    index = num_teams * 4 + j
                    if index >= len(electrika_users):
                        break
                    user = electrika_users[num_teams * 4 + j]
                    user.team = team
                    user.to_be_teamed_up = False
                    user.save()
    except Exception:
        messages.error(request, "Error creating teams!")
        return redirect("electrika_admin_teams")

    messages.success(request, "Successfully created teams!")
    return redirect("electrika_admin_teams")


@login_required
@ensure_group_membership(group_names=["electrika_admin"])
def user_management(request):
    args = {}
    args["users"] = ElectrikaUser.objects.all()
    return render(request, "electrika/admin/users.html", args)


@login_required
@ensure_group_membership(group_names=["electrika_admin"])
def announcements_management(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save()

            mail_option = form.cleaned_data.get("announcement_mailing", "1")
            email_ids = None
            if mail_option == "2":
                # just for team leaders
                if announcement.announcement_type == "A":
                    email_ids = list(
                        Team.objects.values_list("team_leader__user__email", flat=True)
                    )

            elif mail_option == "3":
                # for all members
                if announcement.announcement_type == "A":
                    email_ids = list(
                        ElectrikaUser.objects.values_list("user__email", flat=True)
                    )
                elif announcement.announcement_type == "N":
                    email_ids = list(
                        ElectrikaUser.objects.filter(team=None).values_list(
                            "user__email", flat=True
                        )
                    )
                elif announcement.announcement_type == "T":
                    email_ids = list(
                        ElectrikaUser.objects.filter(team__isnull=False).values_list(
                            "user__email", flat=True
                        )
                    )

            if email_ids is not None:
                send_email(
                    "Announcement | Electrika",
                    "emails/electrika/announcement.html",
                    {"announcement": announcement},
                    bcc=email_ids,
                )

            messages.success(request, "Successfully created announcement!")
            return redirect("electrika_announcements")
        else:
            messages.error(
                request, "Please correct the errors before creating announcement!"
            )
            return redirect("electrika_announcements")
    else:
        form = AnnouncementForm()
        announcements = Announcement.objects.all().order_by("-date_created")

    args = {"form": form, "announcements": announcements}
    return render(request, "electrika/admin/announcements.html", args)


@login_required
@ensure_group_membership(group_names=["electrika_admin"])
def delete_announcement(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    announcement.delete()
    messages.success(request, "Successfully deleted announcement!")
    return redirect("electrika_announcements")
