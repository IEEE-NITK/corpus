from datetime import datetime

from accounts.models import User
from config.models import DATETIME_FORMAT
from config.models import ModuleConfiguration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from skyward_expedition.forms import AnnouncementForm
from skyward_expedition.forms import InviteForm
from skyward_expedition.forms import SEForm
from skyward_expedition.forms import SubmissionForm
from skyward_expedition.forms import TeamCreationForm
from skyward_expedition.models import Announcement
from skyward_expedition.models import Invite
from skyward_expedition.models import SEUser
from skyward_expedition.models import Submission
from skyward_expedition.models import Team

from corpus.decorators import ensure_group_membership
from corpus.decorators import module_enabled


# Create your views here.
def home(request):
    args = {}

    if request.user is not None and request.user.is_authenticated:
        se_user = SEUser.objects.filter(user=request.user).first()
        if se_user is not None:
            args["dashboard"] = True

        if request.user.groups.filter(name="skyward_expedition_admin").exists():
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


@login_required
@module_enabled(module_name="skyward_expedition")
def submission(request):
    team = SEUser.objects.get(user=request.user).team

    try:
        prev_submission = Submission.objects.get(team=team)
    except Submission.DoesNotExist:
        prev_submission = None

    if prev_submission:
        form = SubmissionForm(instance=prev_submission)
    else:
        form = SubmissionForm()

    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.team = team
            submission.save()
            messages.success(request, "Submission made successfully!")
            return redirect("skyward_expedition_dashboard")

    args = {"form": form}

    return render(request, "skyward_expedition/create_submission.html", args)


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def admin(request):
    return render(request, "skyward_expedition/admin/index.html")


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def member_dashboard(request):
    members = SEUser.objects.all()

    members_count = members.count()
    nitk_count = members.filter(nitk_participant=True).count()
    ieee_count = members.filter(ieee_member=True).count()

    args = {
        "members": members,
        "members_count": members_count,
        "nitk_count": nitk_count,
        "ieee_count": ieee_count,
    }

    return render(request, "skyward_expedition/admin/member_dashboard.html", args)


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def teams_dashboard(request):
    teams = Team.objects.all()

    teams_count = teams.count()

    args = {"teams": teams, "teams_count": teams_count}

    return render(request, "skyward_expedition/admin/teams_dashboard.html", args)


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def team_details(request, team_id):
    team = Team.objects.get(id=team_id)
    members = SEUser.objects.filter(team=team)

    args = {"team": team, "members": members}

    return render(request, "skyward_expedition/admin/team_details.html", args)


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def announcements_dashboard(request):
    announcements = Announcement.objects.all().order_by("-pk")

    args = {"announcements": announcements}

    return render(
        request, "skyward_expedition/admin/announcements_dashboard.html", args
    )


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def new_announcement(request):
    form = AnnouncementForm()

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save()
            mail_option = int(form.cleaned_data.get("announcement_mail", "1"))
            announcement.send_email(mail_option)
            messages.success(request, "Announcement added successfully!")
            return redirect("skyward_expedition_announcements_dashboard")

    args = {"form": form}

    return render(request, "skyward_expedition/admin/new_announcement.html", args)


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def edit_announcement(request, announcement_id):
    announcement = Announcement.objects.get(pk=announcement_id)
    form = AnnouncementForm(instance=announcement)

    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()

            messages.success(request, "Announcement updated!")
            return redirect("skyward_expedition_announcements_dashboard")

    args = {"announcement": announcement, "form": form}

    return render(request, "skyward_expedition/admin/edit_announcement.html", args)


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def delete_announcement(request, announcement_id):
    announcement = Announcement.objects.get(pk=announcement_id)
    announcement.delete()

    messages.success(request, "Announcement deleted!")
    return redirect("skyward_expedition_announcements_dashboard")


@login_required
@ensure_group_membership(group_names=["skyward_expedition_admin"])
def submissions_dashboard(request):
    submissions = Submission.objects.all()
    args = {"submissions": submissions}
    return render(request, "skyward_expedition/admin/submissions_dashboard.html", args)
