import re

from django.contrib.auth import get_user_model

from blog.models import Post
from constants import MAX_IMAGE_SIZE
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from virtual_expo.models import Report

from .forms import CorpusCreationForm
from .forms import CorpusLoginForm
from .forms import ExecutiveMemberForm
from .forms import FacultyForm
from .forms import UserForm
from .models import ExecutiveMember
from .models import Faculty

User = get_user_model()



# Create your views here.


def signup(request):
    if request.method == "POST":
        form = CorpusCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "You have been successfully registered. Please sign in!"
            )
            return redirect("accounts_signin")
    else:
        form = CorpusCreationForm()
    args = {"form": form}
    return render(request, "accounts/signup.html", args)


def signin(request):
    next = request.GET.get("next", "")
    if request.method == "POST":
        form = CorpusLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back to Corpus!")
            if next == "":
                return redirect("index")
            else:
                return redirect(next)
        else:
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            if username.endswith("@nitk.edu.in"):
                exec_member = ExecutiveMember.objects.filter(edu_email=username)
            elif username.endswith("@ieee.org"):
                exec_member = ExecutiveMember.objects.filter(ieee_email=username)
            elif re.search(r"^[1-9][0-9]{2}[A-Za-z]{2}[0-9]{3}$", username) is not None:
                exec_member = ExecutiveMember.objects.filter(
                    roll_number=username.upper()
                )
            elif re.search(r"^[0-9]{6,}$", username) is not None:
                exec_member = ExecutiveMember.objects.filter(reg_number=username)
            else:
                exec_member = None

            if exec_member:
                user = authenticate(
                    username=exec_member[0].user.email, password=password
                )
                if user is not None:
                    login(request, user)
                    messages.success(request, "Welcome back to Corpus!")
                    if next == "":
                        return redirect("index")
                    else:
                        return redirect(next)
    else:
        form = CorpusLoginForm()

    args = {"form": form}
    return render(request, "accounts/login.html", args)


def signout(request):
    logout(request)
    messages.success(request, "Successfully signed out.")
    return redirect("index")


def profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    
    try:
        exec_member = ExecutiveMember.objects.get(user=profile_user)
        faculty = None
    except ExecutiveMember.DoesNotExist:
        exec_member = None
        try :
            faculty = Faculty.objects.get(user=profile_user)
        except Faculty.DoesNotExist :
            faculty = None

    # Get Virtual Expo Reports
    if exec_member:
        reports = Report.objects.filter(reportmember__member=exec_member)
        # Get Blogs written by the Executive Member
        blogs = Post.objects.filter(author=exec_member)
    else:
        reports = None
        blogs = None

    args = {
        "exec_member": exec_member,
        "faculty" : faculty,
        "profile_user": profile_user,
        "curr_user": request.user,
        "reports": reports,
        "blogs": blogs,
    }

    return render(request, "accounts/profile.html", args)


@login_required
def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk) # Get the user explicitly by ID
    
    # Authorization check: Ensure logged-in user can only edit their own profile
    if request.user != user:
        messages.warning(request, "You are not authorized to edit this profile.")
        return redirect("index")
    
    # Check if the user has an associated ExecutiveMember record
    try:
        executive_member = ExecutiveMember.objects.get(user=user)
        faculty = None
    except ExecutiveMember.DoesNotExist:
        executive_member = None
        try :
            faculty = Faculty.objects.get(user=user)
        except Faculty.DoesNotExist:
            faculty = None

    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES, instance=user)
        if executive_member:
            executive_member_form = ExecutiveMemberForm(
                request.POST, instance=executive_member
            )
            if user_form.is_valid() and executive_member_form.is_valid():
                user_form.save()
                executive_member_form.save()
                return redirect("accounts_profile", pk=pk)
            
        else:
            if faculty :
                faculty_form = FacultyForm(
                    request.POST, instance=faculty
                )
                if user_form.is_valid() and faculty_form.is_valid():
                    user_form.save()
                    faculty_form.save()
                    return redirect("accounts_profile", pk=pk)
            else :
                if user_form.is_valid():
                    user_form.save()
                    return redirect("accounts_profile", pk=pk)

    else:
        user_form = UserForm(instance=user)
        if executive_member:
            executive_member_form = ExecutiveMemberForm(instance=executive_member)
            faculty_form = None
        else:
            executive_member_form = None
            if faculty :
                faculty_form = FacultyForm(instance=faculty)
            else :
                faculty_form = None    

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "executive_member_form": executive_member_form,
            "faculty_form" : faculty_form,
            "exec_member": executive_member,
            "max_image_size": MAX_IMAGE_SIZE,
        },
    )
