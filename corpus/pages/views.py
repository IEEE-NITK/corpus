from datetime import date,timedelta

from accounts.models import ExecutiveMember
from accounts.models import Faculty
from config.models import ModuleConfiguration
from config.models import SIG
from config.models import Society
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from newsletter.models import Event

from corpus.decorators import module_enabled
from .forms import SIGContentForm
from .forms import SocietyDashboardForm

from django.utils import timezone


def _get_sig_dashboard_permissions(user):
    if not user.is_authenticated:
        return {}

    if user.is_superuser:
        sigs = SIG.objects.exclude(slug__isnull=True)
        return {sig.slug: sig for sig in sigs}

    try:
        exec_member = (
            ExecutiveMember.objects.select_related("sig", "core__post")
            .get(user=user)
        )
    except ExecutiveMember.DoesNotExist:
        return {}

    if not hasattr(exec_member, "core"):
        return {}

    post_name = (exec_member.core.post.name or "").lower()
    if "chair" not in post_name:
        return {}

    if not exec_member.sig.slug:
        return {}

    return {exec_member.sig.slug: exec_member.sig}


def _get_authorized_sig_or_none(request, sig_slug):
    authorized_sigs = _get_sig_dashboard_permissions(request.user)
    return authorized_sigs.get(sig_slug)


def get_active_members():
    try:
        active_batches = ModuleConfiguration.objects.get(module_name="teampage").module_config
    except ModuleConfiguration.DoesNotExist:
        return None

    reg_years = []
    for _k, value in active_batches.items():
        reg_years.append(
            (value % 100) - 4
        )  # Get the year indicated by their roll no / reg no

    query = Q()
    for prefix in reg_years:
        query |= Q(reg_number__startswith=prefix)

    # Executive Members
    members = ExecutiveMember.objects.filter(query)
    return members


def get_alumni():
    """Return number of executive members who were in earlier batches (alumni)."""
    try:
        config = ModuleConfiguration.objects.get(
            module_name="teampage"
        ).module_config
    except ModuleConfiguration.DoesNotExist:
        return None

    # Extract active batches (current members)
    active_reg_years = []
    for _k, value in config.items():
        active_reg_years.append((value % 100) - 4)  # same logic as active members

    # Alumni = all whose reg_number prefix NOT in active_reg_years
    alumni_query = Q()
    for prefix in active_reg_years:
        alumni_query &= ~Q(reg_number__startswith=str(prefix))

    alumni = ExecutiveMember.objects.filter(alumni_query)

    return alumni


def get_event_count():
    """Return total number of events ever conducted."""
    return Event.objects.all().count()


def index(request):
    # Get all societies to render on landing page Societies section
    societies = Society.objects.all()
    members = get_active_members()
    alumnis = get_alumni()
    if members is None:
        members_count = None
    else:
        members_count = members.count()

    if alumnis is None:
        alumni_count = None
    else:
        alumni_count = alumnis.count()

    events_count = get_event_count()
    return render(
        request,
        "pages/index.html",
        {
            "societies": societies,
            "members_count": members_count,
            "alumni_count": alumni_count,
            "events_count": events_count,
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
    societies_linked_to_sig = sig_data.societies.all()
    alumnilogos_linked_to_sig = sig_data.alumni_logos.all()
    today = timezone.now().date()
    past_year = today-timedelta(days=365)
    events_past_year = sig_data.events.filter(
        start_date__range=(past_year, today)
    ).order_by("start_date")
    number_of_members = get_active_members().filter(sig=sig_data).count()
    number_of_events = events_past_year.count()
    can_manage_sig = sig_data.slug in _get_sig_dashboard_permissions(request.user)

    return render(
        request,
        "pages/sig.html",
        {
            "sig": sig_data,
            "societies_linked_to_sig": societies_linked_to_sig,
            "events": events_past_year,
            "alumni_logos": alumnilogos_linked_to_sig,
            "no_of_members": number_of_members,
            "no_of_events": number_of_events,
            "can_manage_sig": can_manage_sig,
        },
    )


@module_enabled("teampage")
def team(request):
    members = get_active_members()
    if members is None:
        messages.error(
            request,
            """
            No active members found. Kindly contact the administrators.
            """
        )
        return redirect("index")

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


@login_required
def sig_dashboard_list(request):
    authorized_sigs = _get_sig_dashboard_permissions(request.user)
    return render(
        request,
        "pages/sig_dashboard_list.html",
        {"authorized_sigs": authorized_sigs.values()},
    )


@login_required
def sig_dashboard(request, sig_slug):
    sig_data = _get_authorized_sig_or_none(request, sig_slug)
    if sig_data is None:
        messages.error(
            request,
            "Permission denied. You can only access dashboards for SIGs you chair.",
        )
        return redirect("sig_dashboard_list")

    sig_form = SIGContentForm(instance=sig_data)
    society_form = SocietyDashboardForm(sig=sig_data)

    invalid_society_form = None
    invalid_society_id = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "update_sig":
            sig_form = SIGContentForm(request.POST, request.FILES, instance=sig_data)
            if sig_form.is_valid():
                sig_form.save()
                messages.success(request, f"{sig_data.name} page details updated.")
                return redirect("sig_dashboard", sig_slug=sig_slug)

        elif action == "create_society":
            society_form = SocietyDashboardForm(request.POST, request.FILES, sig=sig_data)
            if society_form.is_valid():
                society = society_form.save(commit=False)
                society.save()
                society.sigs.add(sig_data)
                society_form.save_faculty_advisors(society=society, sig=sig_data)
                messages.success(request, "Society added to SIG successfully.")
                return redirect("sig_dashboard", sig_slug=sig_slug)

        elif action == "update_society":
            society_id = request.POST.get("society_id")
            society_instance = get_object_or_404(Society, id=society_id, sigs=sig_data)
            edit_form = SocietyDashboardForm(
                request.POST,
                request.FILES,
                instance=society_instance,
                sig=sig_data,
            )
            if edit_form.is_valid():
                society = edit_form.save()
                edit_form.save_faculty_advisors(society=society, sig=sig_data)
                messages.success(request, "Society details updated.")
                return redirect("sig_dashboard", sig_slug=sig_slug)
            invalid_society_form = edit_form
            invalid_society_id = society_instance.id

        elif action == "remove_society":
            society_id = request.POST.get("society_id")
            society = get_object_or_404(Society, id=society_id, sigs=sig_data)
            society.sigs.remove(sig_data)
            Faculty.objects.filter(sig=sig_data, society=society).update(society=None)
            messages.success(request, "Society removed from this SIG.")
            return redirect("sig_dashboard", sig_slug=sig_slug)

        elif action == "clear_society_advisors":
            society_id = request.POST.get("society_id")
            society = get_object_or_404(Society, id=society_id, sigs=sig_data)
            Faculty.objects.filter(sig=sig_data, society=society).update(society=None)
            messages.success(request, "All faculty advisors removed from this society.")
            return redirect("sig_dashboard", sig_slug=sig_slug)

    linked_societies = sig_data.societies.all().order_by("name")
    society_edit_forms = []
    for society in linked_societies:
        if invalid_society_id == society.id and invalid_society_form is not None:
            society_edit_forms.append((society, invalid_society_form))
        else:
            society_edit_forms.append((society, SocietyDashboardForm(instance=society, sig=sig_data)))

    return render(
        request,
        "pages/sig_dashboard.html",
        {
            "sig": sig_data,
            "sig_form": sig_form,
            "society_form": society_form,
            "society_edit_forms": society_edit_forms,
        },
    )
