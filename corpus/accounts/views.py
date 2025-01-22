import re

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .forms import CorpusCreationForm
from .forms import CorpusLoginForm
from .forms import UserForm
from .forms import ExecutiveMemberForm
from .models import ExecutiveMember
# from .models import User
from virtual_expo.models import Report, ReportMember
from blog.models import Post


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
    profile_user = exec_member.user

    # Get Virtual Expo Reports
    reports = Report.objects.filter(reportmember__member=exec_member)

    # Get Blogs written by the Executive Member
    blogs = Post.objects.filter(author=exec_member)

    args = {
        "exec_member": exec_member,
        "profile_user": profile_user,
        "curr_user": request.user,
        "reports": reports,
        "blogs": blogs,
    }

    return render(request, "accounts/profile.html", args)

@login_required
def edit_profile(request, roll_no):
    user = request.user  # Get the currently logged-in user
    
    # Check if the user has an associated ExecutiveMember record
    try:
        executive_member = ExecutiveMember.objects.get(roll_number=roll_no, user=user)
    except ExecutiveMember.DoesNotExist:
        raise PermissionDenied("You are not authorized to edit this profile.")

    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user)
        executive_member_form = ExecutiveMemberForm(request.POST, instance=executive_member)
        
        if user_form.is_valid() and executive_member_form.is_valid():
            user_form.save()
            # Handle hiding GitHub/LinkedIn if checkboxes are selected
            hide_linkedin = request.POST.get('hide_linkedin', False)
            hide_github = request.POST.get('hide_github', False)
            
            if hide_linkedin:
                executive_member.hide_linkedin = True
            else:
                executive_member.hide_linkedin = False
            
            if hide_github:
                executive_member.hide_github = True
            else:
                executive_member.hide_github = False
            executive_member_form.save()
            return redirect('accounts_profile', roll_no=roll_no)

    else:
        user_form = UserForm(instance=user)
        executive_member_form = ExecutiveMemberForm(instance=executive_member)

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'user_form': user_form,
            'executive_member_form': executive_member_form,
            'exec_member': executive_member,
        }
    )