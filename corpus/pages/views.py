from accounts.models import ExecutiveMember
from accounts.models import Faculty
from config.models import SIG
from config.models import Society
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
    # ExeCom Members
    ieee_core = ExecutiveMember.objects.filter(
        core__isnull=False, core__post__is_execom=True, core__post__is_sac=False
    ).order_by("core__post__priority")

    # CompSoc Core Members
    compsoc_core = ExecutiveMember.objects.filter(
        core__isnull=False,
        sig__name="CompSoc",
        core__post__is_execom=False,
        core__post__is_sac=False,
    ).order_by("core__post__priority")

    # Diode Core Members
    diode_core = ExecutiveMember.objects.filter(
        core__isnull=False,
        sig__name="Diode",
        core__post__is_execom=False,
        core__post__is_sac=False,
    ).order_by("core__post__priority")

    # Piston Core Members
    piston_core = ExecutiveMember.objects.filter(
        core__isnull=False,
        sig__name="Piston",
        core__post__is_execom=False,
        core__post__is_sac=False,
    ).order_by("core__post__priority")

    # SAC Core Members
    sac_core = ExecutiveMember.objects.filter(
        core__isnull=False, core__post__is_execom=False, core__post__is_sac=True
    ).order_by("core__post__priority")

    # Faculty Members
    faculty = Faculty.objects.all()

    # Executive Members
    compsoc_members = (
        ExecutiveMember.objects.filter(sig__name="CompSoc")
        .exclude(pk__in=ieee_core.values("pk"))
        .exclude(pk__in=compsoc_core.values("pk"))
        .exclude(pk__in=sac_core.values("pk"))
    )
    diode_members = (
        ExecutiveMember.objects.filter(sig__name="Diode")
        .exclude(pk__in=ieee_core.values("pk"))
        .exclude(pk__in=diode_core.values("pk"))
        .exclude(pk__in=sac_core.values("pk"))
    )
    piston_members = (
        ExecutiveMember.objects.filter(sig__name="Piston")
        .exclude(pk__in=ieee_core.values("pk"))
        .exclude(pk__in=piston_core.values("pk"))
        .exclude(pk__in=sac_core.values("pk"))
    )

    context = {
        "compsoc_members": compsoc_members,
        "diode_members": diode_members,
        "piston_members": piston_members,
        "ieee_core": ieee_core,
        "compsoc_core": compsoc_core,
        "diode_core": diode_core,
        "piston_core": piston_core,
        "sac_core": sac_core,
        "faculty": faculty,
    }
    return render(request, "pages/team.html", context)


def farewell(request):
    return render(request, "pages/farewell.html")
