from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from virtual_expo.forms import ReportForm
from virtual_expo.models import Report
from virtual_expo.models import ReportMember

from corpus.decorators import ensure_exec_membership


@ensure_exec_membership()
def dashboard(request):
    reports = Report.objects.filter(reportmember__member=request.exec_member)

    args = {"reports": reports}

    return render(request, "virtual_expo/members/dashboard.html", args)


@ensure_exec_membership()
def preview_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    report_members = ReportMember.objects.filter(report=report)

    args = {"report": report, "members": report_members, "preview": True}

    return render(request, "virtual_expo/report.html", args)


@ensure_exec_membership()
def new_report(request):
    form = ReportForm()

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_at = timezone.now()
            report.save()

            ReportMember.objects.create(report=report, member=request.exec_member)

            messages.success(request, "Report saved successfully!")
            return redirect("virtual_expo_members_dashboard")

    args = {"form": form}

    return render(request, "virtual_expo/members/new_report.html", args)
