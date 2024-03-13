from accounts.models import Core
from accounts.models import ExecutiveMember
from accounts.models import Faculty
from config.models import SIG
from config.models import Society
from django.db.models import Q
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
    compsoc_members = ExecutiveMember.objects.filter(
        Q(core__isnull=True) and Q(sig__name="CompSoc")
    )
    diode_members = ExecutiveMember.objects.filter(
        Q(core__isnull=True) and Q(sig__name="Diode")
    )
    piston_members = ExecutiveMember.objects.filter(
        Q(core__isnull=True) and Q(sig__name="Piston")
    )
    ieee_core = Core.objects.filter(sig__name="ExeCom").order_by("post")
    compsoc_core = Core.objects.filter(sig__name="CompSoc").order_by("post")
    diode_core = Core.objects.filter(sig__name="Diode").order_by("post")
    piston_core = Core.objects.filter(sig__name="Piston").order_by("post")

    faculty = Faculty.objects.all()
    context = {
        "compsoc_members": compsoc_members,
        "diode_members": diode_members,
        "piston_members": piston_members,
        "ieee_core": ieee_core,
        "compsoc_core": compsoc_core,
        "diode_core": diode_core,
        "piston_core": piston_core,
        "faculty": faculty,
    }
    return render(request, "pages/team.html", context)

def farewell(request):
    return render(request, "pages/farewell.html")
