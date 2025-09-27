from blog.forms import BlogForm
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from corpus.decorators import ensure_exec_membership


@login_required
@ensure_exec_membership()
def dashboard(request):
    blogs = Post.objects.filter(author=request.exec_member).order_by("-pk")
    admin_user = request.user.groups.filter(name="blog_admin").exists()

    if request.method == "POST":
        blog_id = int(request.POST.get("blog_id"))
        blog = Post.objects.get(pk=blog_id)
        blog.ready_for_approval = True
        blog.save()
        messages.success(request, "Sent blog for approval!")
        return redirect("blog_dashboard")

    args = {"blogs": blogs, "admin": admin_user}
    # args = {"blogs": blogs}

    return render(request, "blog/members/dashboard.html", args)


@login_required
@ensure_exec_membership()
def new_blog(request):
    form = BlogForm()

    if request.method == "POST":
        print(request.POST)

        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.created_at = timezone.localtime()
            blog.author = request.user.executivemember
            blog.save()

            form.save_m2m()

            messages.success(request, "Blog saved successfully!")
            return redirect("blog_dashboard")

    args = {"form": form}

    return render(request, "blog/members/new_blog.html", args)


@login_required
@ensure_exec_membership()
def edit_blog(request, slug):
    blog = Post.objects.get(slug=slug)
    # members = ExecutiveMember.objects.filter(reportmember__report=blog)

    form = BlogForm(instance=blog)

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            return redirect("blog_dashboard")

    args = {"blog": blog, "form": form}

    return render(request, "blog/members/edit_blog.html", args)


@ensure_exec_membership()
def preview_blog(request, slug):
    blog = Post.objects.get(slug=slug)

    args = {"individual_post": blog, "preview": True}

    return render(request, "blog/full_post.html", args)


@login_required
@ensure_exec_membership()
def approver_dashboard(request):
    blogs = Post.objects.filter(approver=request.exec_member, approved=False).order_by(
        "-pk"
    )

    if request.method == "POST":
        blog_id = int(request.POST.get("blog_id"))
        blog = Post.objects.get(pk=blog_id)
        if blog.approver == request.exec_member:
            blog.approved = True
            blog.published_date = timezone.localtime()
            blog.save()
            blog.publish()
            messages.success(request, "Blog marked as approved!")
            return redirect("blog_approver_dashboard")
        else:
            messages.error(request, "You are not the approver for this blog.")
            return redirect("blog_dashboard")

    args = {"blogs": blogs}

    return render(request, "blog/members/approver_dashboard.html", args)
