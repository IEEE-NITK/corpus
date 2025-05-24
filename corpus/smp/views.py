from accounts.models import ExecutiveMember
from config.models import SIG
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from smp.forms import ProgramFilterForm
from smp.forms import SubmissionForm
from smp.models import Program
from smp.models import ProgramMember
from smp.models import Submission
from smp.models import Upload

from corpus.decorators import ensure_exec_membership


def home(request):
    try:
        ExecutiveMember.objects.get(user=request.user.id)
        exec_member = True
    except ExecutiveMember.DoesNotExist:
        exec_member = False

    years = list(Program.objects.values_list("year", flat=True).distinct())
    return render(
        request, "smp/home.html", {"years": years, "exec_member": exec_member}
    )


@login_required
def programs_by_year(request, year):
    programs = Program.objects.filter(year=year, hide_program=False).order_by("-pk")
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

    return render(
        request,
        "smp/programs_by_year.html",
        {"programs": programs.distinct(), "year": year, "form": form},
    )


@login_required
def program(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    return render(
        request,
        "smp/program.html",
        {
            "program": program,
            "mentors": program.mentors(),
            "mentees": program.mentees(),
        },
    )


@ensure_exec_membership()
def preview_program(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    return render(
        request,
        "smp/program.html",
        {
            "program": program,
            "mentors": program.mentors(),
            "mentees": program.mentees(),
            "preview": True,
        },
    )


@login_required
def upload_list(request, program_id):
    program = get_object_or_404(Program, pk=program_id)

    try:
        program_member = ProgramMember.objects.get(program=program, member=request.user)
    except ProgramMember.DoesNotExist:
        messages.error(request, "You have not been added to this program.")
        return redirect("smp_program", program_id=program.id)

    uploads = Upload.objects.filter(program=program).order_by("-uploaded_at")
    return render(
        request,
        "smp/upload_list.html",
        {
            "program": program,
            "mentors": program.mentors(),
            "mentees": program.mentees(),
            "uploads": uploads,
            "member_type": program_member.member_type,
        },
    )


@login_required
def view_upload(request, upload_id):
    upload = get_object_or_404(Upload, id=upload_id)
    return render(
        request,
        "smp/mentors/view_upload.html",
        {"upload": upload, "program": upload.program},
    )


@login_required
def view_submission(request, upload_id):
    upload = get_object_or_404(Upload, id=upload_id)
    program = upload.program

    try:
        ProgramMember.objects.get(program=program, member=request.user)
    except ProgramMember.DoesNotExist:
        messages.error(request, "You are not a part of this program.")
        return redirect("smp_program", program_id=program.id)

    mentors = program.mentors()
    mentor_users = [mentor.user for mentor in mentors]
    mentees = program.mentees()

    if request.user in mentor_users:
        submissions = Submission.objects.filter(assignment=upload)
        return render(
            request, "smp/mentors/submission_list.html", {"submissions": submissions}
        )

    elif request.user in mentees:
        submission = Submission.objects.filter(
            user=request.user, assignment=upload
        ).first()

        if request.method == "POST":
            if submission:
                form = SubmissionForm(request.POST, instance=submission)
            else:
                # Create the submission instance with assignment and user pre-set
                submission = Submission(user=request.user, assignment=upload)
                form = SubmissionForm(request.POST, instance=submission)

            if form.is_valid():
                form.save()
                messages.success(request, "Submission successful!")
                return redirect("upload_list", program_id=program.id)
        else:
            form = SubmissionForm(instance=submission)

        return render(
            request,
            "smp/view_submission.html",
            {
                "upload": upload,
                "submission": submission,
                "form": form,
                "program": program,
            },
        )

    else:
        messages.error(request, "You are not authorized to view this submission.")
        return redirect("smp_program", program_id=program.id)


@login_required
def create_submission(request, upload_id):
    upload = get_object_or_404(Upload, id=upload_id)

    if upload.upload_type != "Assignment":
        messages.error(request, "Submissions are only allowed for assignments.")
        return redirect("smp_program", program_id=upload.program.id)

    program = upload.program

    try:
        program_member = ProgramMember.objects.get(program=program, member=request.user)
    except ProgramMember.DoesNotExist:
        messages.error(request, "You are not a member of this program.")
        return redirect("smp_program", program_id=program.id)

    if program_member.member_type != "Mentee":
        messages.error(request, "Only mentees can submit assignments.")
        return redirect("smp_program", program_id=program.id)

    existing_submission = Submission.objects.filter(
        user=request.user, assignment=upload
    ).first()
    if existing_submission:
        messages.info(request, "You have already submitted this assignment.")
        return redirect("view_submission", upload_id=upload.id)

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        submission = form.save(commit=False)
        submission.user = request.user
        submission.assignment = upload

        if form.is_valid():
            try:
                submission.full_clean()
                submission.save()
                messages.success(request, "Submission saved successfully.")
                return redirect("view_submission", upload_id=upload.id)
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = SubmissionForm()

    return render(
        request,
        "smp/create_submission.html",
        {"form": form, "upload": upload, "program": program},
    )
