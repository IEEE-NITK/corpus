from config.models import SIG
from django.db.models import Count
from django.shortcuts import render
from virtual_expo.forms import ReportFilterForm
from virtual_expo.models import Report
from virtual_expo.models import ReportType

from corpus.decorators import ensure_group_membership


@ensure_group_membership(group_names=["virtual_expo_admin"])
def dashboard(request):
    reports = Report.objects.all()

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

    args = {"reports": reports, "form": form}

    return render(request, "virtual_expo/admin/dashboard.html", args)
