from datetime import datetime

from django.shortcuts import render
from accounts.models import User
from config.models import DATETIME_FORMAT
from config.models import ModuleConfiguration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from impulse.models import Announcement
from impulse.models import ImpulseUser
from impulse.models import Team
from impulse.forms import ImpulseForm
from impulse.forms import TeamCreationForm
from impulse.forms import AnnouncementForm
from impulse.forms import Member2Form
from impulse.forms import PaymentProofForm

# from impulse.forms import TeamCreationForm



from corpus.decorators import ensure_group_membership
from corpus.decorators import module_enabled

# Create your views here.
def home(request):
    # check group_membership, if admin redirect to admin page
    args = {}
    if request.user.groups.filter(name="impulse_admin").exists():
        args = {"admin": True}
    return render(
        request,
        "impulse/home.html",
        args,
    )

@login_required
@module_enabled(module_name="impulse")
def index(request):
    args = {}
    try :
        impulse_user = ImpulseUser.objects.get(user=request.user)
        args["impulse_user"] = impulse_user
    except ImpulseUser.DoesNotExist:
        messages.error(request, "Please register for Impulse first!")
        return redirect("impulse_register")
    
    # Check if already part of team
    if impulse_user.team is not None:
        args["in_team"] = True

        team = impulse_user.team
        
        args["is_member2"] = impulse_user.is_member2
        if impulse_user.is_member2:
            args['team_count'] = 2
        else:
            args['team_count'] = 1

        args["member"] = impulse_user

        args["team"] = team

        if not impulse_user.is_member2:
            args["member2_form"] = Member2Form()
    else:
        args["in_team"] = False
        args["team_creation_form"] = TeamCreationForm()
        
    config = ModuleConfiguration.objects.get(module_name="impulse").module_config

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

    args["payment_proof_form"] = PaymentProofForm()

    args["registration_active"] = registration_active
    args["announcements"] = Announcement.objects.all().order_by("-date_created")

    return render(request, "impulse/index.html", args)


@login_required
@module_enabled(module_name="impulse")
def register(request):

    config = ModuleConfiguration.objects.get(module_name="impulse").module_config

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
        messages.error(request, "Registration for Impulse is not active yet!")
        return redirect("index")
    
    try:
        impulse_user = ImpulseUser.objects.get(user=request.user)
        messages.error(request, "You have already registered for Impulse!")
        return redirect("impulse_index")
    except ImpulseUser.DoesNotExist:
        pass

    if request.method == "POST":
        form = ImpulseForm(request.POST)
        print("Form received")
        if form.is_valid():
            print("Form is valid")
            impulse_user = form.save(commit=False)
            print("Form saved")
            impulse_user.user = request.user
            impulse_user.save()
            print("Impulse user saved")
            messages.success(request, "Successfully registered for Impulse!")
            return redirect("impulse_index")
        else:
            messages.error(request, "Please correct the errors before registering!")

    else:
        form = ImpulseForm()

    args = {"form": form}
    print("Creating registration form")
    return render(request, "impulse/register.html", args)


@login_required
@module_enabled(module_name="impulse")
def create_team(request):
    if request.method == "POST":
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            impulse_user = ImpulseUser.objects.get(user=request.user)
            team.team_leader = impulse_user

            if impulse_user.from_nitk or impulse_user.ieee_member:
                team.payment_status = "E"
            else:
                team.payment_status = "U"

            team.save() 
            impulse_user.team = team
            impulse_user.save()
            messages.success(request, "Successfully created team!")
            return redirect("impulse_index")
        else:
            messages.error(request, "Please correct the errors before creating team!")
            return redirect("impulse_index")
        
@login_required
@module_enabled(module_name="impulse")
def add_member(request):
    if request.method == "POST":
        form = Member2Form(request.POST)
        if form.is_valid():
            impulse_user = ImpulseUser.objects.get(user=request.user)
            # Save the member2 details in the form into the impulse_user
            impulse_user.is_member2 = True
            impulse_user.member2_name = form.cleaned_data["member2_name"]
            impulse_user.member2_email = form.cleaned_data["member2_email"]
            impulse_user.member2_from_nitk = form.cleaned_data["member2_from_nitk"]
            impulse_user.member2_college_name = form.cleaned_data["member2_college_name"]
            impulse_user.member2_roll_no = form.cleaned_data["member2_roll_no"]
            impulse_user.member2_phone = form.cleaned_data["member2_phone"]
            impulse_user.member2_ieee_member = form.cleaned_data["member2_ieee_member"]
            impulse_user.member2_ieee_membership_no = form.cleaned_data["member2_ieee_membership_no"]
            impulse_user.save()

            if impulse_user.member2_from_nitk or impulse_user.member2_ieee_member:
                team = impulse_user.team
                team.payment_status = "E"
                team.save()
            messages.success(request, "Successfully added member!")
            return redirect("impulse_index")
        else:
            messages.error(request, "Please correct the errors before adding member!")
            return redirect("impulse_index")
    else:
        form = Member2Form()
        args = {"form": form}
        return render(request, "impulse/add_member.html", args)

@login_required
@module_enabled(module_name="impulse")
def upload_payment_proof(request):
    if request.method == "POST":
        impulse_user = ImpulseUser.objects.get(user=request.user)
        team = Team.objects.get(team_leader=impulse_user)
        
        if team.payment_proof is not None:
            team.payment_proof.delete()
        team.payment_proof = request.FILES["payment_proof"]
        if team.payment_proof is None:
            messages.error(request, "Please upload a file!")
            return redirect("impulse_index")
        team.save()
        messages.success(request, "Successfully uploaded payment proof!")
        return redirect("impulse_index")
    else:
        return redirect("impulse_index")

@login_required
@module_enabled(module_name="impulse")
def delete_payment_proof(request):
    impulse_user = ImpulseUser.objects.get(user=request.user)
    team = Team.objects.get(team_leader=impulse_user)
    team.payment_proof.delete()
    team.save()
    messages.success(request, "Successfully deleted payment proof!")
    return redirect("impulse_index")

@login_required
@ensure_group_membership(group_names=["impulse_admin"])
def admin(request):
    return render(request, "impulse/admin/admin.html", {})

@login_required
@ensure_group_membership(group_names=["impulse_admin"])
def team_management(request):
    args = {}
    args["teams"] = Team.objects.all()
    return render(request, "impulse/admin/teams.html", args)

@login_required
@ensure_group_membership(group_names=["impulse_admin"])
def team_page(request, pk):
    args = {}
    team = Team.objects.get(pk=pk)
    args["team"] = team
    members = ImpulseUser.objects.filter(team=team)
    for member in members:
        args["member"] = member

    return render(request, "impulse/admin/team_page.html", args)

@login_required
@ensure_group_membership(group_names=["impulse_admin"])
def user_management(request):
    args = {}
    args["users"] = ImpulseUser.objects.all()
    return render(request, "impulse/admin/users.html", args)

@login_required
@ensure_group_membership(group_names=["impulse_admin"])
def announcements_management(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully created announcement!")
            return redirect("impulse_announcements")
        else:
            messages.error(request, "Please correct the errors before creating announcement!")
            return redirect("impulse_announcements")
    else:
        form = AnnouncementForm()
        announcements = Announcement.objects.all().order_by("-date_created")

    args = {"form": form, "announcements": announcements}
    return render(request, "impulse/admin/announcements.html", args)


@login_required
@ensure_group_membership(group_names=["impulse_admin"])
def delete_announcement(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    announcement.delete()
    messages.success(request, "Successfully deleted announcement!")
    return redirect("impulse_announcements")

@login_required
@ensure_group_membership(group_names=["impulse_admin"])
def mark_payment_complete(request, pk):
    team = Team.objects.get(pk=pk)
    team.payment_status = "P"
    team.save()
    messages.success(request, "Successfully marked payment as complete!")
    return redirect("impulse_admin_team_page", pk=pk)

@login_required
@ensure_group_membership(group_names=["impulse_admin"])
def mark_payment_incomplete(request, pk):
    team = Team.objects.get(pk=pk)
    team.payment_status = "U"
    team.save()
    messages.success(request, "Successfully marked payment as incomplete!")
    return redirect("impulse_admin_team_page", pk=pk)