from accounts.models import ExecutiveMember
from config.models import SIG
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    user = request.user

    is_member = ProgramMember.objects.filter(program=program, member=user).exists()
    is_coordinator = user.groups.filter(name__in=["smp_coordinator"]).exists()

    if not is_member and not is_coordinator:
        messages.error(request, "You have not been added to this program.")
        return redirect("smp_program", program_id=program.id)

    if is_coordinator:
        member_type = "Mentor"
    else:
        program_member = ProgramMember.objects.get(program=program, member=request.user)
        member_type = program_member.member_type

    if member_type == "Mentor":

        if request.method == "POST":
            upload_id = int(request.POST.get("upload_id"))
            upload = Upload.objects.get(id=upload_id)

            if "delete" in request.POST:
                upload.delete()
                messages.success(request, "Upload has been deleted.")

            return redirect("upload_list", program_id=program.id)

    uploads = Upload.objects.filter(program=program).order_by("-uploaded_at")
    return render(
        request,
        "smp/upload_list.html",
        {
            "program": program,
            "mentors": program.mentors(),
            "mentees": program.mentees(),
            "uploads": uploads,
            "member_type": member_type,
        },
    )


@login_required
def view_upload(request, upload_id):
    upload = get_object_or_404(Upload, id=upload_id)
    user = request.user
    program = upload.program

    is_member = ProgramMember.objects.filter(program=program, member=user).exists()
    is_coordinator = user.groups.filter(name__in=["smp_coordinator"]).exists()

    if not is_member and not is_coordinator:
        messages.error(request, "You have not been added to this program.")
        return redirect("smp_program", program_id=program.id)

    return render(
        request,
        "smp/mentors/view_upload.html",
        {"upload": upload, "program": program},
    )


@login_required
def view_submission(request, upload_id):
    upload = get_object_or_404(Upload, id=upload_id)
    user = request.user
    program = upload.program

    is_member = ProgramMember.objects.filter(program=program, member=user).exists()
    is_coordinator = user.groups.filter(name__in=["smp_coordinator"]).exists()

    if not is_member and not is_coordinator:
        messages.error(request, "You have not been added to this program.")
        return redirect("smp_program", program_id=program.id)

    mentors = program.mentors()
    mentor_users = [mentor.user for mentor in mentors]
    mentees = program.mentees()

    if user in mentor_users or is_coordinator:
        submissions = Submission.objects.filter(assignment=upload)

        if request.method == "POST":
            submission_id = int(request.POST.get("submission_id"))
            submission = Submission.objects.get(id=submission_id, assignment=upload)

            if "delete" in request.POST:
                submission.delete()
                messages.success(request, "Program has been deleted.")

            return redirect("view_submission", upload_id=upload.id)
        return render(
            request,
            "smp/mentors/submission_list.html",
            {"submissions": submissions, "admin": is_coordinator},
        )

    elif user in mentees:
        submission = Submission.objects.filter(
            user=request.user, assignment=upload
        ).first()

        form = None

        if request.method == "POST":
            if "add" in request.POST:
                if submission:
                    form = SubmissionForm(request.POST, instance=submission)
                else:
                    submission = Submission(user=request.user, assignment=upload)
                    form = SubmissionForm(request.POST, instance=submission)

                if form.is_valid():
                    form.save()
                    messages.success(request, "Submission successful!")
                    return redirect("upload_list", program_id=program.id)

            elif "delete" in request.POST:
                submission_id_str = request.POST.get("submission_id")
                if submission_id_str and submission_id_str.isdigit():
                    submission_id = int(submission_id_str)
                    try:
                        submission_to_delete = Submission.objects.get(
                            id=submission_id, assignment=upload
                        )

                        if (
                            submission_to_delete.user == request.user
                            or request.user in mentors
                        ):
                            submission_to_delete.delete()
                            messages.success(
                                request, "Submission deleted successfully."
                            )
                        else:
                            messages.error(
                                request,
                                "You do not have permission to delete this submission.",
                            )
                    except Submission.DoesNotExist:
                        messages.error(request, "Submission does not exist.")
                else:
                    messages.error(request, "Invalid submission id.")

                return redirect("upload_list", program_id=program.id)

        # If form is still None (e.g., GET request or after delete), initialize it
        if form is None:
            form = SubmissionForm(instance=submission)

        return render(
            request,
            "smp/view_submission.html",
            {
                "upload": upload,
                "submission": submission,
                "form": form,
                "program": program,
                "admin": is_coordinator,
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

    submission = Submission.objects.filter(user=request.user, assignment=upload).first()

    if submission:
        messages.info(request, "You have already submitted this assignment.")
        return redirect("view_submission", upload_id=upload.id)

    if request.method == "POST":
        if submission:
            form = SubmissionForm(request.POST, instance=submission)
        else:
            submission = Submission(user=request.user, assignment=upload)
            form = SubmissionForm(request.POST, instance=submission)

        if form.is_valid():
            form.save()
            messages.success(request, "Submission saved successfully.")
            return redirect("view_submission", upload_id=upload.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SubmissionForm(instance=submission)

    return render(
        request,
        "smp/create_submission.html",
        {"form": form, "upload": upload, "program": program},
    )
