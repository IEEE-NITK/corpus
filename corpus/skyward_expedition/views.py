from datetime import datetime

from config.models import DATETIME_FORMAT
from config.models import ModuleConfiguration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from skyward_expedition.forms import SEForm
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
    return render(request, "skyward_expedition/dashboard.html")
