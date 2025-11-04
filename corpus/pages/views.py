from accounts.models import ExecutiveMember
from accounts.models import Faculty
from config.models import SIG, ModuleConfiguration
from config.models import Society
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from corpus.decorators import module_enabled
from django.db.models import Q
from accounts.models import ExecutiveMember


def get_active_members():
    active_batches = get_object_or_404(ModuleConfiguration, module_name="teampage").module_config

    reg_years = []
    for _k, value in active_batches.items():
        reg_years.append((value % 100) - 4) # Get the year indicated by their roll no / reg no

    query = Q()
    for prefix in reg_years:
        query |= Q(reg_number__startswith=prefix)
    
    # Executive Members
    members = ExecutiveMember.objects.filter(query)
    return members

def index(request):
    # Get all societies to render on landing page Societies section
    societies = Society.objects.all()
    members_count = get_active_members().count()
    return render(
        request,
        "pages/index.html",
        {
            "societies": societies,
            "members_count": members_count,
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
    events_linked_to_sig = sig_data.events.all().order_by('start_date')
    alumnilogos_linked_to_sig = sig_data.alumni_logos.all()
    number_of_members = get_active_members().filter(sig=sig_data).count()
    number_of_events = events_linked_to_sig.count()

    args = {
        "sig": sig_data,
        "societies_linked_to_sig": societies_linked_to_sig,
        "events": events_linked_to_sig,
        "alumni_logos": alumnilogos_linked_to_sig,
        "no_of_members": number_of_members,
        "no_of_events": number_of_events,
    }

    return render(request, "pages/sig.html", args)


@module_enabled("teampage")
def team(request):
    members = get_active_members()

    # ExeCom Members
    ieee_core = members.filter(
        core__isnull=False, 
        core__post__is_execom=True, 
        core__post__is_sac=False,  
    ).order_by("core__post__priority")

    # CompSoc Core Members
    compsoc_core = members.filter(
        core__isnull=False,
        sig__name="CompSoc",
        core__post__is_execom=False,
        core__post__is_sac=False,
    ).order_by("core__post__priority")

    # Diode Core Members
    diode_core = members.filter(
        core__isnull=False,
        sig__name="Diode",
        core__post__is_execom=False,
        core__post__is_sac=False,    
    ).order_by("core__post__priority")

    # Piston Core Members
    piston_core = members.filter(
        core__isnull=False,
        sig__name="Piston",
        core__post__is_execom=False,
        core__post__is_sac=False,
    ).order_by("core__post__priority")

    # SAC Core Members
    sac_core = members.filter(
        core__isnull=False, 
        core__post__is_execom=False, 
        core__post__is_sac=True,
    ).order_by("core__post__priority")

    # Faculty Members
    faculty = Faculty.objects.all()

    compsoc_members = (
        members.filter(sig__name="CompSoc")
        .exclude(pk__in=ieee_core.values("pk"))
        .exclude(pk__in=compsoc_core.values("pk"))
        .exclude(pk__in=sac_core.values("pk"))
    )
    diode_members = (
        members.filter(sig__name="Diode")
        .exclude(pk__in=ieee_core.values("pk"))
        .exclude(pk__in=diode_core.values("pk"))
        .exclude(pk__in=sac_core.values("pk"))
    )
    piston_members = (
        members.filter(sig__name="Piston")
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
