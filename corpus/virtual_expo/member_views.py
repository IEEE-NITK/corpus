from accounts.models import ExecutiveMember
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from virtual_expo.forms import ReportForm
from virtual_expo.forms import ReportMemberForm
from virtual_expo.models import Report
from virtual_expo.models import ReportMember

from corpus.decorators import ensure_exec_membership


@login_required
@ensure_exec_membership()
def dashboard(request):
    reports = Report.objects.filter(reportmember__member=request.exec_member).order_by(
        "-pk"
    )
    admin_user = request.user.groups.filter(name="virtual_expo_admin").exists()

    if request.method == "POST":
        report_id = int(request.POST.get("report_id"))
        report = Report.objects.get(pk=report_id)
        report.ready_for_approval = True
        report.save()
        messages.success(request, "Sent report for approval!")
        return redirect("virtual_expo_members_dashboard")

    args = {"reports": reports, "admin": admin_user}

    return render(request, "virtual_expo/members/dashboard.html", args)


@login_required
@ensure_exec_membership()
def new_report(request):
    form = ReportForm()

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_at = timezone.localtime()
            report.save()

            ReportMember.objects.create(report=report, member=request.exec_member)

            messages.success(request, "Report saved successfully!")
            return redirect("virtual_expo_members_dashboard")

    args = {"form": form}

    return render(request, "virtual_expo/members/new_report.html", args)


@login_required
@ensure_exec_membership()
def edit_report(request, report_id):
    report = Report.objects.get(pk=report_id)
    members = ExecutiveMember.objects.filter(reportmember__report=report)

    if request.exec_member not in members:
        messages.error(request, "You have not been added to this report.")
        return redirect("virtual_expo_members_dashboard")

    form = ReportForm(instance=report)

    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "Report updated successfully!")
            return redirect("virtual_expo_members_dashboard")

    args = {"report": report, "form": form}

    return render(request, "virtual_expo/members/edit_report.html", args)


@login_required
@ensure_exec_membership()
def add_members(request, report_id):
    report = Report.objects.get(pk=report_id)
    members = ExecutiveMember.objects.filter(reportmember__report=report)

    if request.exec_member not in members:
        messages.error(request, "You have not been added to this report.")
        return redirect("virtual_expo_members_dashboard")

    form = ReportMemberForm(initial={"report": report})

    if request.method == "POST":
        if "add" in request.POST:
            form = ReportMemberForm(request.POST)
            form.instance.report = report
            if form.is_valid():
                try:
                    form.save()
                except IntegrityError:
                    messages.error(request, "Member already added to the project.")
                    return redirect(
                        "virtual_expo_members_add_members", report_id=report.id
                    )

                messages.success(request, "Member added to project.")
                return redirect("virtual_expo_members_add_members", report_id=report.id)
        elif "edit" in request.POST:
            report_id = int(request.POST.get("report_id"))
            member_id = int(request.POST.get("member_id"))
            report = Report.objects.get(pk=report_id)
            member = ExecutiveMember.objects.get(pk=member_id)

            if member == request.exec_member:
                messages.error(request, "You cannot remove yourself from the project.")
                return redirect("virtual_expo_members_add_members", report_id=report.id)

            try:
                report_member = ReportMember.objects.get(report=report, member=member)
                report_member.delete()
            except ReportMember.DoesNotExist:
                messages.error(request, "Member does not exist for this project.")
                return redirect("virtual_expo_members_add_members", report_id=report.id)

            messages.success(request, "Members edited in project.")
            return redirect("virtual_expo_members_add_members", report_id=report.id)

    args = {
        "form": form,
        "members": members,
        "report": report,
    }

    return render(request, "virtual_expo/members/add_members.html", args)


@login_required
@ensure_exec_membership()
def approver_dashboard(request):
    reports = Report.objects.filter(
        approver=request.exec_member, approved=False
    ).order_by("-pk")

    if request.method == "POST":
        report_id = int(request.POST.get("report_id"))
        report = Report.objects.get(pk=report_id)
        if report.approver == request.exec_member:
            report.approved = True
            report.approved_at = timezone.localtime()
            report.save()
            messages.success(request, "Report marked as approved!")
            return redirect("virtual_expo_members_approver_dashboard")
        else:
            messages.error(request, "You are not the approver for this report.")
            return redirect("virtual_expo_members_approver_dashboard")

    args = {"reports": reports}

    return render(request, "virtual_expo/members/approver_dashboard.html", args)
