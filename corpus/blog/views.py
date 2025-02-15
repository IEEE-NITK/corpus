from accounts.models import ExecutiveMember
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone

from .models import Post
from .models import Tag


# view for the blog list page
def post_list(request):
    try:
        ExecutiveMember.objects.get(user=request.user.id)
        exec_member = True
    except ExecutiveMember.DoesNotExist:
        exec_member = False

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "-published_date"
    )
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(
        request,
        "blog/post_list.html",
        {
            "posts": posts,
            "tags": tags,
            "page_obj": page_obj,
            "exec_member": exec_member,
        },
    )


def full_post(request, slug):
    individual_post = get_object_or_404(
        Post.objects.filter(published_date__lte=timezone.now()), slug=slug
    )
    return render(request, "blog/full_post.html", {"individual_post": individual_post})


# view for blogs filtered on the basis of tags
def tagged_blog(request, specific_tag):
    required_tag = get_object_or_404(Tag, id=specific_tag)
    specific_tag_blogs = Post.objects.filter(
        blog_tag=specific_tag, published_date__lte=timezone.now()
    ).order_by("-published_date")
    paginator = Paginator(specific_tag_blogs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(
        request,
        "blog/tagged_post.html",
        {
            "specific_tag_blogs": specific_tag_blogs,
            "required_tag": required_tag,
            "page_obj": page_obj,
            "tags": tags,
        },
    )
