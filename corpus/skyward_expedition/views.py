from datetime import datetime

from accounts.models import User
from config.models import DATETIME_FORMAT
from config.models import ModuleConfiguration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from skyward_expedition.forms import InviteForm
from skyward_expedition.forms import SEForm
from skyward_expedition.forms import TeamCreationForm
from skyward_expedition.models import Announcement
from skyward_expedition.models import Invite
from skyward_expedition.models import SEUser

from corpus.decorators import module_enabled


# Create your views here.
def home(request):
    args = {}

    if request.user is not None and request.user.is_authenticated:
        se_user = SEUser.objects.filter(user=request.user).first()
        if se_user is not None:
            args["dashboard"] = True

        if request.user.groups.filter(name__in="se_admin").exists():
            args["admin"] = True

    return render(request, "skyward_expedition/home.html", args)


@login_required
@module_enabled(module_name="skyward_expedition")
def register(request):
    config = ModuleConfiguration.objects.get(
        module_name="skyward_expedition"
    ).module_config

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
        messages.error(
            request, "Registration for Skyward Expedition is not active yet."
        )
        return redirect("index")

    try:
        se_user = SEUser.objects.get(user=request.user)
        if se_user:
            messages.info(request, "You have already registered!")
            return redirect("skyward_expedition_dashboard")
    except SEUser.DoesNotExist:
        pass

    if request.method == "POST":
        form = SEForm(request.POST)
        if form.is_valid():
            se_user = form.save(commit=False)
            se_user.user = request.user
            se_user.save()
            messages.success(request, "Registration successful!")
            return redirect("skyward_expedition_dashboard")
    else:
        form = SEForm()

    args = {"form": form}

    return render(request, "skyward_expedition/register.html", args)


@login_required
@module_enabled(module_name="skyward_expedition")
def dashboard(request):
    args = {}
    try:
        se_user = SEUser.objects.get(user=request.user)
        args["se_user"] = se_user
    except SEUser.DoesNotExist:
        messages.error(request, "Please register first!")
        return redirect("skyward_expedition_register")

    if se_user.team is not None:
        args["in_team"] = True

        team = se_user.team
        members = SEUser.objects.filter(team=team)

        args["team"] = team
        args["members"] = members

        if team.team_leader == se_user:
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
        invites = Invite.objects.filter(invite_email=se_user.user.email)
        args["invites_for_user"] = invites

    config = ModuleConfiguration.objects.get(
        module_name="skyward_expedition"
    ).module_config

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

    return render(request, "skyward_expedition/dashboard.html", args)


@login_required
@module_enabled(module_name="skyward_expedition")
def create_team(request):
    if request.method == "POST":
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            se_user = SEUser.objects.get(user=request.user)
            team.team_leader = se_user
            team.save()

            se_user.team = team
            se_user.save()

            messages.success(request, "Team created successfully!")
            return redirect("skyward_expedition_dashboard")
    else:
        messages.error(request, "Illegal Request")
        return redirect("skyward_expedition_dashboard")


@login_required
@module_enabled(module_name="skyward_expedition")
def create_invite(request):
    se_user = SEUser.objects.get(user=request.user)
    if request.method == "POST":
        form = InviteForm(request.POST)
        if form.is_valid():
            if request.user.email == form.cleaned_data["invite_email"]:
                messages.error(request, "You cannot invite yourself!")
                return redirect("skyward_expedition_dashboard")

            try:
                user = User.objects.get(email=form.cleaned_data["invite_email"])
                invited_emb_user = SEUser.objects.get(user=user)
                if invited_emb_user.team is not None:
                    messages.error(request, "User is already in a team!")
                    return redirect("skyward_expedition_dashboard")
            except (User.DoesNotExist, SEUser.DoesNotExist):
                pass

            try:
                invite = Invite.objects.get(
                    inviting_team=se_user.team,
                    invite_email=form.cleaned_data["invite_email"],
                )
                messages.error(request, "Invite has already been sent!")
                return redirect("skyward_expedition_dashboard")
            except Invite.DoesNotExist:
                pass

            invite_counts = Invite.objects.filter(inviting_team=se_user.team).count()
            team_members = SEUser.objects.filter(team=se_user.team).count()
            config = ModuleConfiguration.objects.get(
                module_name="skyward_expedition"
            ).module_config
            max_count = int(config["max_team_size"])

            if invite_counts >= max_count or team_members >= max_count:
                messages.error(request, "Maximum team member limit reached!")
                return redirect("skyward_expedition_dashboard")

            invite = form.save(commit=False)
            inviting_team = se_user.team
            invite.inviting_team = inviting_team
            invite.save()

            messages.success(request, "Invite sent!")
            return redirect("skyward_expedition_dashboard")
    messages.error(request, "Illegal Request")
    return redirect("skyward_expedition_dashboard")


@login_required
@module_enabled(module_name="skyward_expedition")
def accept_invite(request, pk):
    invite = Invite.objects.get(pk=pk)
    team_members = SEUser.objects.filter(team=invite.inviting_team).count()
    config = ModuleConfiguration.objects.get(
        module_name="skyward_expedition"
    ).module_config
    max_count = int(config["max_team_size"])

    if team_members >= max_count:
        invite.delete()
        messages.error(request, "Maximum team member limit reached!")
        return redirect("skyward_expedition_dashboard")

    if request.user.email != invite.invite_email:
        messages.error(request, "Illegal request")
        return redirect("skyward_expedition_dashboard")

    se_user = SEUser.objects.get(user=request.user)
    se_user.team = invite.inviting_team
    se_user.save()

    Invite.objects.filter(invite_email=request.user.email).delete()

    messages.success(request, "Invite accepted!")
    return redirect("skyward_expedition_dashboard")


@login_required
@module_enabled(module_name="skyward_expedition")
def delete_invite(request, pk):
    invite = Invite.objects.get(pk=pk)
    invite.delete()

    messages.success(request, "Invite deleted!")
    return redirect("skyward_expedition_dashboard")
