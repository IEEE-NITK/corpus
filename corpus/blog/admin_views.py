from accounts.models import ExecutiveMember
from blog.forms import AdminBlogForm
from blog.forms import BlogFilterForm
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone

from corpus.decorators import ensure_group_membership


@login_required
@ensure_group_membership(group_names=["blog_admin"])
def dashboard(request):
    blogs = Post.objects.all().order_by("-pk")  # Fetch all blogs, ordered by latest

    form = BlogFilterForm(request.GET)
    if form.is_valid():
        print("Selected SIGs:", form.cleaned_data.get("sig"))

        author_id = int(form.cleaned_data.get("author"))
        if author_id != 0:
            blogs = blogs.filter(author=ExecutiveMember.objects.get(pk=author_id))

        sig_ids = form.cleaned_data.get("sig")
        if sig_ids:
            blogs = blogs.filter(blog_tag__in=sig_ids).distinct()

    args = {"blogs": blogs, "form": form}
    return render(request, "blog/admin/dashboard.html", args)


@login_required
@ensure_group_membership(group_names=["blog_admin"])
def manage(request, blog_id):
    blog = Post.objects.get(pk=blog_id)
    form = AdminBlogForm(instance=blog)

    if request.method == "POST":
        form = AdminBlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():

            blog = form.save(commit=False)

            if blog.approved and not blog.approved_at:
                blog.approved_at = timezone.now()
            blog.publish()

            messages.success(request, "Blog Updated Successfully!")
            return redirect("blog_admin_dashboard")

    args = {"blog": blog, "form": form}

    return render(request, "blog/admin/manage.html", args)
