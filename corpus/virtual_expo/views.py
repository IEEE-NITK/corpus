from datetime import datetime

from django.contrib import messages

from accounts.models import ExecutiveMember
from config.models import SIG, ModuleConfiguration
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from virtual_expo.forms import ReportFilterForm
from virtual_expo.models import Report
from virtual_expo.models import ReportMember
from virtual_expo.models import ReportType

from corpus.decorators import ensure_exec_membership, ensure_view_current_envision


# Create your views here.
def home(request):
    try:
        ExecutiveMember.objects.get(user=request.user.id)
        exec_member = True
    except ExecutiveMember.DoesNotExist:
        exec_member = False

    years = list(Report.objects.values_list("year", flat=True).distinct())

    args = {"years": years, "exec_member": exec_member}

    return render(request, "virtual_expo/home.html", args)


@ensure_view_current_envision()
def reports_by_year(request, year, can_view_current_envision):
    reports = Report.objects.filter(year=year, approved=True).order_by("-pk")
    config = ModuleConfiguration.objects.get(module_name="virtual_expo").module_config

    if not can_view_current_envision and year == datetime.now().year:
        reports = reports.exclude(report_type=config.get("envision_report_type"))

    form = ReportFilterForm(request.GET)
    if form.is_valid():
        report_type = int(form.cleaned_data.get("report_type"))
        if report_type != 0:
            reports = reports.filter(report_type=ReportType.objects.get(pk=report_type))
            if not can_view_current_envision and year == datetime.now().year:
                reports = reports.exclude(report_type=config.get("envision_report_type"))

        sig = int(form.cleaned_data.get("sig"))
        if sig == -1:
            reports = reports.annotate(
                sig_count=Count("reportmember__member__sig", distinct=True)
            ).filter(sig_count__gte=2)
        elif sig != 0:
            reports = reports.filter(reportmember__member__sig=SIG.objects.get(pk=sig))

    reports = reports.distinct()
    args = {"reports": reports, "year": year, "form": form}

    return render(request, "virtual_expo/reports_by_year.html", args)


@ensure_view_current_envision()
def report(request, report_id, can_view_current_envision):
    report = get_object_or_404(Report, pk=report_id)
    if not can_view_current_envision and report.year == datetime.now().year:
        config = ModuleConfiguration.objects.get(module_name="virtual_expo").module_config
        if report.report_type.id == config.get("envision_report_type"):
            messages.error(
                request,
                "Report does not exist",
            )
            return redirect("index")

    report_members = ReportMember.objects.filter(report=report)

    args = {"report": report, "members": report_members}

    return render(request, "virtual_expo/report.html", args)


@ensure_exec_membership()
def preview_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    report_members = ReportMember.objects.filter(report=report)

    args = {"report": report, "members": report_members, "preview": True}

    return render(request, "virtual_expo/report.html", args)
