from config.models import SIG
from config.models import Society
from accounts.models import Core
from accounts.models import Faculty
from accounts.models import ExecutiveMember
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from django.db.models import Case, When, Value, CharField

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
    members = ExecutiveMember.objects.filter(
    Q(user__core__isnull=True) | Q(user__core=None)
)
    ieee_core_posts = [
        "Convenor", 
        "Chairperson", 
        "Vice Chairperson",
        "Secretary",
        "Joint Secretary",
        "Treasurer(Branch)",
        "Treasurer(Institute)",
        "Webmaster",
        "Media Lead",
        "Outreach Lead",
        "Envision Lead",
        "Labs Lead",  
        ]
    

    compsoc_core_posts = [
        "CompSoc Chair",
        "CompSoc Vice Chair",
        "CompSoc Secretary",
        "CompSoc Project Head",
        "CompSoc Project Coordinator",
        "CIS Chair",
        "CIS Secretary",
        "CIS Project Head",

    ]

    diode_core_posts = [
        "Diode Chair",
        "SPS Chair",
        "SPS Vice Chair",
        "SPS Secretary",
        "CAS Chair",
        "CAS Vice Chair",
        "CAS Secretary",
        "RAS Chair",
        "RAS Secretary",
    ]

    piston_core_posts = [
        "Piston Chair",
        "Piston Vice Chair",
        "Piston Secretary",
        "Piston Project Head",
        "IAS Chair",
        "IAS Secretary",
    ]

    ieee_core = Core.objects.filter(post__in=ieee_core_posts).order_by(
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

    compsoc_core = Core.objects.filter(post__in=compsoc_core_posts).order_by(
        Case(
            When(post="CompSoc Chair", then=Value(1)),
            When(post="CompSoc Vice Chair", then=Value(2)),
            When(post="CompSoc Secretary", then=Value(3)),
            When(post="CompSoc Project Head", then=Value(4)),
            When(post="CompSoc Project Coordinator", then=Value(5)),
            When(post="CIS Chair", then=Value(6)),
            When(post="CIS Secretary", then=Value(7)),
            When(post="CIS Project Head", then=Value(8)),
            When(post="Webmaster", then=Value(9)),
        )
    )

    diode_core = Core.objects.filter(post__in=diode_core_posts).order_by(
        Case(
            When(post="Diode Chair", then=Value(1)),
            When(post="SPS Chair", then=Value(2)),
            When(post="SPS Vice Chair", then=Value(3)),
            When(post="SPS Secretary", then=Value(4)),
            When(post="CAS Chair", then=Value(5)),
            When(post="CAS Vice Chair", then=Value(6)),
            When(post="CAS Secretary", then=Value(7)),
            When(post="RAS Chair", then=Value(8)),
            When(post="RAS Secretary", then=Value(9)),
        )
    )

    piston_core = Core.objects.filter(post__in=piston_core_posts).order_by(
        Case(
            When(post="Piston Chair", then=Value(1)),
            When(post="Piston Vice Chair", then=Value(2)),
            When(post="Piston Secretary", then=Value(3)),
            When(post="Piston Project Head", then=Value(4)),
            When(post="IAS Chair", then=Value(5)),
            When(post="IAS Secretary", then=Value(6)),
        )
    ) 
    

    faculty = Faculty.objects.all()
    context = {
        "members":members,
        "compsoc_core":compsoc_core,
        "diode_core":diode_core,
        "piston_core":piston_core,
        "faculty":faculty,
    }
    return render(request, "pages/team.html", context)