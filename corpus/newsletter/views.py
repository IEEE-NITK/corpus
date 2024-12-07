from django.shortcuts import render
from .models import NewsPost

# Create your views here.

def home(request):
    posts = NewsPost.objects.all()
    context = {'posts': posts}
    return render(request, "newsletter/home.html", context)
