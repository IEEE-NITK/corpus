from accounts.models import ExecutiveMember
from blog.forms import AdminBlogForm
from blog.forms import BlogFilterForm
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from corpus.decorators import ensure_group_membership


@login_required
@ensure_group_membership(group_names=["blog_admin"])
def dashboard(request):
    blogs = Post.objects.all().order_by("-pk")  # Fetch all blogs, ordered by latest

    form = BlogFilterForm(request.GET)
    if form.is_valid():

        author_id = int(form.cleaned_data.get("author"))
        if author_id != 0:
            author = get_object_or_404(ExecutiveMember, pk=author_id)
            blogs = blogs.filter(author=author)

        tag_ids = form.cleaned_data.get("tag")
        if tag_ids:
            blogs = blogs.filter(blog_tag__in=tag_ids).distinct()

    args = {"blogs": blogs, "form": form}
    return render(request, "blog/admin/dashboard.html", args)


@login_required
@ensure_group_membership(group_names=["blog_admin"])
def manage(request, blog_id):
    blog = get_object_or_404(Post, pk=blog_id)
    form = AdminBlogForm(instance=blog)

    if request.method == "POST":
        form = AdminBlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():

            blog = form.save(commit=False)

            try:
                approver_member = ExecutiveMember.objects.get(user=request.user)
            except ExecutiveMember.DoesNotExist:
                approver_member = None

            blog.publish(approver=approver_member)

            messages.success(request, "Blog Updated Successfully!")
            return redirect("blog_admin_dashboard")

    args = {"blog": blog, "form": form}

    return render(request, "blog/admin/manage.html", args)
