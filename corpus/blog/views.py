from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Tag,Post
from django.template import Context,Template
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import blog_form

# view for the blog list page
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(posts,9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    tags = Tag.objects.all()
    return render(request,'blog/post_list.html',{'posts':posts,'tags':tags,'page_obj':page_obj})

def full_post(request,slug):
    individual_post = Post.objects.filter(published_date__lte=timezone.now()).get(slug=slug)
    return render(request,'blog/full_post.html',{'individual_post':individual_post})

#view for blogs filtered on the basis of tags
def tagged_blog(request,specific_tag):
    specific_tag_blogs= Post.objects.filter(blog_tag=specific_tag,published_date__lte=timezone.now())
    required_tag = Tag.objects.get(id=specific_tag)
    paginator = Paginator(specific_tag_blogs,9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'blog/tagged_post.html',{'specific_tag_blogs':specific_tag_blogs,'required_tag':required_tag,'page_obj':page_obj})


