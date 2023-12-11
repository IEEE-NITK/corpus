from datetime import datetime

from config.models import DATETIME_FORMAT
from config.models import ModuleConfiguration
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from embedathon.forms import EmbedathonForm
from embedathon.models import EmbedathonUser

from corpus.decorators import module_enabled


# Create your views here.


@login_required
@module_enabled(module_name="embedathon")
def index(request):
    try:
        embedathon_user = EmbedathonUser.objects.get(user=request.user)
    except EmbedathonUser.DoesNotExist:
        messages.error(request, "Please register for Embedathon first!")
        return redirect("embedathon_register")

    args = {"embedathon_user": embedathon_user}

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
