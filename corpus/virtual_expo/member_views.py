from django.shortcuts import render
from virtual_expo.models import Report

from corpus.decorators import ensure_exec_membership


@ensure_exec_membership()
def dashboard(request):
    reports = Report.objects.filter(reportmember__member=request.exec_member)

    args = {"reports": reports}

    return render(request, "virtual_expo/members/dashboard.html", args)
