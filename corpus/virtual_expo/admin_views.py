from accounts.models import ExecutiveMember
from config.models import SIG
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import redirect
from django.shortcuts import render
from virtual_expo.forms import AdminReportForm
from virtual_expo.forms import ReportFilterForm
from virtual_expo.models import Report
from virtual_expo.models import ReportType

from corpus.decorators import ensure_group_membership


@login_required
@ensure_group_membership(group_names=["virtual_expo_admin"])
def dashboard(request):
    reports = Report.objects.all().order_by("-pk")

    form = ReportFilterForm(request.GET)
    if form.is_valid():
        year = int(form.cleaned_data.get("year"))
        if year != 0:
            reports = reports.filter(year=year)

        report_type = int(form.cleaned_data.get("report_type"))
        if report_type != 0:
            reports = reports.filter(report_type=ReportType.objects.get(pk=report_type))

        sig = int(form.cleaned_data.get("sig"))
        if sig == -1:
            reports = reports.annotate(
                sig_count=Count("reportmember__member__sig", distinct=True)
            ).filter(sig_count__gte=2)
        elif sig != 0:
            reports = reports.filter(reportmember__member__sig=SIG.objects.get(pk=sig))

    reports = reports.distinct()
    args = {"reports": reports, "form": form}

    return render(request, "virtual_expo/admin/dashboard.html", args)


@login_required
@ensure_group_membership(group_names=["virtual_expo_admin"])
def manage(request, report_id):
    report = Report.objects.get(pk=report_id)
    members = ExecutiveMember.objects.filter(reportmember__report=report)
    form = AdminReportForm(instance=report)

    if request.method == "POST":
        form = AdminReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Report Updated Successfully!")
            return redirect("virtual_expo_admin_dashboard")

    args = {"report": report, "form": form, "members": members}

    return render(request, "virtual_expo/admin/manage.html", args)



