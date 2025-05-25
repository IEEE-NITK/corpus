from accounts.models import ExecutiveMember
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from smp.forms import ProgramForm
from smp.forms import ProgramMemberForm
from smp.forms import UploadForm
from smp.models import Program
from smp.models import ProgramMember
from smp.models import Upload

from corpus.decorators import ensure_exec_membership


@login_required
@ensure_exec_membership()
def dashboard(request):
    programs = Program.objects.filter(
        programmember__member=request.exec_member.user
    ).order_by("-pk")

    admin_user = request.user.groups.filter(name="smp_coordinator").exists()

    if request.method == "POST":
        program_id = int(request.POST.get("program_id"))
        action = request.POST.get("action")
        program = get_object_or_404(Program, pk=program_id)

        if action == "hide_program":
            if not program.hide_program:
                program.hide_program = True
                program.save()
                messages.success(request, "Program has been hidden.")
        elif action == "show_program":
            if program.hide_program:
                program.hide_program = False
                program.save()
                messages.success(request, "Program is now visible.")

        return redirect("smp_mentors_dashboard")

    return render(
        request,
        "smp/mentors/dashboard.html",
        {"programs": programs, "admin": admin_user},
    )


@login_required
@ensure_exec_membership()
def new_program(request):
    form = ProgramForm()

    if request.method == "POST":
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            program = form.save(commit=False)
            program.hide_program = True
            program.save()

            ProgramMember.objects.create(
                program=program, member=request.exec_member.user, member_type="Mentor"
            )

            messages.success(request, "Program saved successfully!")
            return redirect("smp_mentors_dashboard")

    args = {"form": form}

    return render(request, "smp/mentors/new_program.html", args)


@login_required
@ensure_exec_membership()
def edit_program(request, program_id):
    program = Program.objects.get(pk=program_id)
    mentors = program.mentors()

    if request.exec_member not in mentors:
        messages.error(request, "You have not been added to this program.")
        return redirect("smp_mentors_dashboard")

    form = ProgramForm(instance=program)

    if request.method == "POST":
        form = ProgramForm(request.POST, request.FILES, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully!")
            return redirect("smp_mentors_dashboard")

    args = {"program": program, "form": form}

    return render(request, "smp/mentors/edit_program.html", args)


@login_required
@ensure_exec_membership()
def add_members(request, program_id):
    program = Program.objects.get(pk=program_id)
    mentors = program.mentors()
    mentees = program.mentees()

    if request.exec_member not in mentors:
        messages.error(request, "You have not been added to this program.")
        return redirect("smp_mentors_dashboard")

    form = ProgramMemberForm(initial={"program": program})

    if request.method == "POST":
        if "add" in request.POST:
            form = ProgramMemberForm(request.POST)
            form.instance.program = program

            if form.is_valid():
                member = form.cleaned_data["member"]

                # Set member_type automatically to "Mentor"
                program_member = form.save(commit=False)
                program_member.member_type = "Mentor"

                # Safety check (optional)
                if not ExecutiveMember.objects.filter(user=member).exists():
                    messages.error(
                        request, "Only Executive Members can be added as mentors."
                    )
                    return redirect("smp_mentors_add_members", program_id=program.id)

                try:
                    program_member.save()
                except IntegrityError:
                    messages.error(request, "Member already added to the program.")
                    return redirect("smp_mentors_add_members", program_id=program.id)

                messages.success(request, "Member added to program.")
                return redirect("smp_mentors_add_members", program_id=program.id)

        elif "edit" in request.POST:
            program_id = int(request.POST.get("program_id"))
            member_id = int(request.POST.get("member_id"))
            program = Program.objects.get(pk=program_id)
            member = User.objects.get(pk=member_id)

            if member == request.exec_member.user:
                messages.error(request, "You cannot remove yourself from the program.")
                return redirect("smp_mentors_add_members", program_id=program.id)

            try:
                program_member = ProgramMember.objects.get(
                    program=program, member=member
                )
                program_member.delete()
            except ProgramMember.DoesNotExist:
                messages.error(request, "Member does not exist for this program.")
                return redirect("smp_mentors_add_members", program_id=program.id)

            messages.success(request, "Members edited in program.")
            return redirect("smp_mentors_add_members", program_id=program.id)

    args = {
        "form": form,
        "mentors": mentors,
        "mentees": mentees,
        "program": program,
    }

    return render(request, "smp/mentors/add_members.html", args)


@login_required
@ensure_exec_membership()
def uploads(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    exec_member = get_object_or_404(ExecutiveMember, user=request.user)
    mentors = program.mentors()

    if exec_member not in mentors:
        messages.error(request, "You have not been added to this program.")
        return redirect("smp_mentors_dashboard")

    form = UploadForm()

    if request.method == "POST":
        if "add" in request.POST:
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                upload = form.save(commit=False)
                upload.program = program
                upload.upload_user = exec_member
                upload.save()
                messages.success(request, "Upload successful!")
                return redirect("smp_mentors_dashboard")

        elif "delete" in request.POST:
            upload_id = int(request.POST.get("upload_id", 0))
            try:
                upload = Upload.objects.get(id=upload_id, program=program)

                if upload.upload_user == request.user or exec_member in mentors:
                    upload.delete()
                    messages.success(request, "Upload deleted successfully.")
                else:
                    messages.error(
                        request, "You do not have permission to delete this upload."
                    )
            except Upload.DoesNotExist:
                messages.error(request, "Upload does not exist.")
            return redirect("smp_mentors_add_upload", program_id=program.id)

    uploads = Upload.objects.filter(program=program).order_by("-uploaded_at")

    args = {"uploads": uploads, "form": form, "program": program}

    return render(request, "smp/mentors/upload.html", args)
