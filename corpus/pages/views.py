from accounts.models import Core
from accounts.models import ExecutiveMember
from accounts.models import Faculty
from config.models import SIG
from config.models import Society
from django.db.models import Case
from django.db.models import Q
from django.db.models import Value
from django.db.models import When
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
    members = ExecutiveMember.objects.filter(Q(core__isnull=True) | Q(core=None))
    ieee_core = Core.objects.filter(sig__name="ExeCom").order_by(
        Case(
            When(post="Convenor", then=Value(1)),
            When(post="Chairperson", then=Value(2)),
            When(post="Vice Chairperson", then=Value(3)),
            When(post="Secretary", then=Value(4)),
            When(post="Joint Secretary", then=Value(5)),
            When(post="Treasurer(Branch)", then=Value(6)),
            When(post="Treasurer(Institute)", then=Value(7)),
            When(post="Webmaster", then=Value(8)),
            When(post="Media Lead", then=Value(9)),
            When(post="Outreach Lead", then=Value(10)),
            When(post="Envision Lead", then=Value(11)),
            When(post="Labs Lead", then=Value(12)),
            When(post="WiE Chair", then=Value(13)),
        )
    )

    compsoc_core = Core.objects.filter(sig__name="CompSoc").order_by("post")
    diode_core = Core.objects.filter(sig__name="Diode").order_by("post")
    piston_core = Core.objects.filter(sig__name="Piston").order_by("post")

    faculty = Faculty.objects.all()
    context = {
        "members": members,
        "ieee_core": ieee_core,
        "compsoc_core": compsoc_core,
        "diode_core": diode_core,
        "piston_core": piston_core,
        "faculty": faculty,
    }
    return render(request, "pages/team.html", context)

def farewell(request):
    return render(request, "pages/farewell.html")
