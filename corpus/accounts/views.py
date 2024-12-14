import re

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .forms import CorpusCreationForm
from .forms import CorpusLoginForm
from .models import ExecutiveMember
from virtual_expo.models import Report, ReportMember

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

def profile(request, roll_no):
    exec_member = get_object_or_404(ExecutiveMember, roll_number=roll_no)
    user = exec_member.user

    # Get Virtual Expo Reports
    reports = Report.objects.filter(reportmember__member=exec_member)


    args = {
        "exec_member": exec_member,
        "user": user,
        "reports": reports
    }

    return render(request, "accounts/profile.html", args)