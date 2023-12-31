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
from corpus.decorators import ensure_group_membership
from corpus.decorators import module_enabled

def home(request):
    args = {}
    # Checking if user is Impulse_admin group member
    if request.user.groups.filter(name="impulse_admin").exists():
        args = {"admin": True}
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

    registration_done = (reg_end_datetime < datetime.now())

    args["registration_active"] = registration_active
    args["registration_done"] = registration_done

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
    
    if impulse_user.team is not None:
        args["in_team"] = True

        args["team_creation_form"] = TeamCreationForm(instance=impulse_user.team)

        team = impulse_user.team
        
        args["is_member2"] = team.is_member
        args["team_count"] = 1 + team.is_member
        args["member"] = impulse_user
        args["team"] = team
        args["payment_status"] = team.payment_status

        pay_status = "Not Registered"

        if args["payment_status"] == "E" or args["payment_status"] == "P":
            pay_status = "Complete"
        elif args["payment_status"] == "U":
            pay_status = "Incomplete"

        if not team.is_member:
            args["member2_form"] = Member2Form()
        else:
            args["member2_form"] = Member2Form(instance=impulse_user.team)
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

    try :
        if pay_status == "Complete":
            announcements = Announcement.objects.filter(announcement_type__in=["A", "P"])
        elif pay_status == "Incomplete":
            announcements = Announcement.objects.filter(announcement_type__in=["A", "U"])
        else:
            announcements = Announcement.objects.filter(announcement_type__in=["A", "N"])
    except:
        announcements = Announcement.objects.filter(announcement_type__in=["A", "N"])

    announcements = announcements.order_by("-date_created")

    args["announcements"] = announcements

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
        if form.is_valid():
            impulse_user = form.save(commit=False)
            impulse_user.user = request.user
            impulse_user.save()
            messages.success(request, "Successfully registered for Impulse!")
            return redirect("impulse_index")
        else:
            messages.error(request, "Please correct the errors before registering!")

    else:
        form = ImpulseForm()

    args = {"form": form}
    return render(request, "impulse/register.html", args)

@login_required
@module_enabled(module_name="impulse")
def create_team(request):
    if request.method == "POST":
        form = TeamCreationForm(request.POST)
        impulse_user = ImpulseUser.objects.get(user=request.user)
        if impulse_user.team is not None:
            if form.is_valid():
                team = impulse_user.team
                team.team_name = form.cleaned_data["team_name"]
                team.save()
                messages.success(request, "Successfully updated team name!")
                return redirect("impulse_index")
        else:
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
        updation = False
        if form.is_valid():
            impulse_user = ImpulseUser.objects.get(user=request.user)
            team = impulse_user.team
            if impulse_user.team is None:
                messages.error(request, "Please create a team first!")
                return redirect("impulse_index")
            if team.is_member:
                updation = True
            else:
                team.is_member = True

            team.member_name = form.cleaned_data["member_name"]
            team.member_email = form.cleaned_data["member_email"]
            team.member_from_nitk = form.cleaned_data["member_from_nitk"]
            team.member_college_name = form.cleaned_data["member_college_name"]
            team.member_roll_no = form.cleaned_data["member_roll_no"]
            team.member_phone = form.cleaned_data["member_phone"]
            team.member_ieee_member = form.cleaned_data["member_ieee_member"]
            team.member_ieee_membership_no = form.cleaned_data["member_ieee_membership_no"]
                
            if team.member_from_nitk or team.member_ieee_member:
                team.payment_status = "E"

            team.save()
            
            if updation:
                messages.success(request, "Successfully updated member details!")
            else:
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
def edit_announcement(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited announcement!")
            return redirect("impulse_announcements")
        else:
            messages.error(request, "Please correct the errors before editing announcement!")
            return redirect("impulse_announcements")
    else:
        form = AnnouncementForm(instance=announcement)

    args = {"form": form}
    return render(request, "impulse/admin/edit_announcement.html", args)


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