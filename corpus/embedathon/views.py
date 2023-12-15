from datetime import datetime

from config.models import DATETIME_FORMAT
from config.models import ModuleConfiguration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from embedathon.forms import EmbedathonForm
from embedathon.forms import InviteForm
from embedathon.forms import TeamCreationForm
from embedathon.models import EmbedathonUser
from embedathon.models import Invite

from corpus.decorators import module_enabled


# Create your views here.


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
                invite = Invite.objects.get(
                    inviting_team=embedathon_user.team,
                    invite_email=form.cleaned_data["invite_email"],
                )
                messages.error(request, "Invite has already been sent!")
                return redirect("embedathon_index")
            except Invite.DoesNotExist:
                pass

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
    if request.user.email != invite.invite_email:
        messages.error(request, "Illegal request")
        return redirect("embedathon_index")

    embedathon_user = EmbedathonUser.objects.get(user=request.user)
    embedathon_user.team = invite.inviting_team
    embedathon_user.save()

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
