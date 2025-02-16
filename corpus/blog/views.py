
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import Context
from django.template import Template
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone

from .models import Post
from .models import Tag


# view for the blog list page (also handles blog filtering based on SIG)
def post_list(request, specific_tag=None):
    if(specific_tag):
        posts = Post.objects.filter(
        blog_tag=specific_tag, published_date__lte=timezone.now()
        ).order_by("-published_date")
        required_tag = Tag.objects.get(id=specific_tag)
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "-published_date"
        )
        required_tag=None
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(
        request,
        "blog/post_list.html",
        {
            
            "posts": posts,
            "required_tag": required_tag,
            "page_obj": page_obj,
            "tags":tags,
        },
    )


def full_post(request, slug):
    individual_post = Post.objects.filter(published_date__lte=timezone.now()).get(
        slug=slug
    )
    return render(request, "blog/full_post.html", {"individual_post": individual_post})


