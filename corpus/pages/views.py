from config.models import SIG
from config.models import Society
from accounts.models import Core
from accounts.models import Faculty
from accounts.models import ExecutiveMember
from django.shortcuts import get_object_or_404
from django.shortcuts import render


def index(request):
    # Get all societies to render on landing page Societies section
    societies = Society.objects.all()

    return render(
        request,
        "pages/index.html",
        {
            "societies": societies,
        },
    )


def about_us(request):
    societies = Society.objects.all()

    return render(
        request,
        "pages/about_us.html",
        {
            "socieites": societies,
        },
    )


def sig(request, sig_name):
    sig_data = get_object_or_404(SIG, slug=sig_name)

    # Retrieve the related society details using the SIG instance
    societies_linked_to_sig = sig_data.societies.all()

    args = {
        "sig": sig_data,
        "societies_linked_to_sig": societies_linked_to_sig,
    }

    return render(request, "pages/sig.html", args)


def team(request):
    members = ExecutiveMember.objects.all()
    core = Core.objects.all()
    faculty = Faculty.objects.all()
    context = {
        "members":members,
        "core":core,
        "faculty":faculty,
    }
    return render(request, "pages/team.html", context)

def farewell(request):
    return render(request, "pages/farewell.html")
