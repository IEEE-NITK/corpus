from accounts.models import User
from config.models import SIG
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import redirect
from django.shortcuts import render
from smp.forms import AdminProgramMemberForm
from smp.forms import ProgramFilterForm
from smp.forms import ProgramForm
from smp.models import Program
from smp.models import ProgramMember

from corpus.decorators import ensure_group_membership


@login_required
@ensure_group_membership(group_names=["smp_coordinator"])
def dashboard(request):
    programs = Program.objects.all().order_by("-pk")

    form = ProgramFilterForm(request.GET)
    if form.is_valid():
        try:
            sig = int(form.cleaned_data.get("sig"))
            if sig == -1:
                programs = programs.annotate(
                    sig_count=Count(
                        "programmember__member__executivemember__sig", distinct=True
                    )
                ).filter(sig_count__gte=2)
            elif sig != 0:
                sig_obj = SIG.objects.filter(pk=sig).first()

                if sig_obj:
                    programs = programs.annotate(
                        sig_count=Count(
                            "programmember__member__executivemember__sig", distinct=True
                        )
                    ).filter(
                        sig_count=1, programmember__member__executivemember__sig=sig_obj
                    )

        except (ValueError, TypeError):
            pass
    programs = programs.distinct()
    args = {"programs": programs, "form": form}

    return render(request, "smp/admin/dashboard.html", args)


@login_required
@ensure_group_membership(group_names=["smp_coordinator"])
def add_members(request, program_id):
    program = Program.objects.get(pk=program_id)
    mentors = program.mentors()
    mentees = program.mentees()

    form = AdminProgramMemberForm(initial={"program": program})

    if request.method == "POST":
        if "add" in request.POST:
            form = AdminProgramMemberForm(request.POST)
            form.instance.program = program
            if form.is_valid():
                try:
                    form.save()
                except IntegrityError:
                    messages.error(request, "Member already added to the program.")
                    return redirect("smp_admin_add_members", program_id=program.id)

                messages.success(request, "Member added to program.")
                return redirect("smp_admin_add_members", program_id=program.id)
        elif "edit" in request.POST:
            program_id = int(request.POST.get("program_id"))
            member_id = int(request.POST.get("member_id"))
            program = Program.objects.get(pk=program_id)
            member = User.objects.get(pk=member_id)

            try:
                program_member = ProgramMember.objects.get(
                    program=program, member=member
                )
                program_member.delete()
            except ProgramMember.DoesNotExist:
                messages.error(request, "Member does not exist for this program.")
                return redirect("smp_admin_add_members", program_id=program.id)

            messages.success(request, "Members edited in program.")
            return redirect("smp_admin_add_members", program_id=program.id)

    args = {
        "form": form,
        "mentors": mentors,
        "mentees": mentees,
        "program": program,
    }

    return render(request, "smp/admin/add_members.html", args)


@login_required
@ensure_group_membership(group_names=["smp_coordinator"])
def manage(request, program_id):
    program = Program.objects.get(pk=program_id)
    form = ProgramForm(instance=program)

    if request.method == "POST":
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully!")
            return redirect("smp_admin_dashboard")

    is_smp_coordinator = request.user.groups.filter(name="smp_coordinator").exists()

    args = {
        "program": program,
        "form": form,
        "admin": is_smp_coordinator,
    }

    return render(request, "smp/mentors/edit_program.html", args)
