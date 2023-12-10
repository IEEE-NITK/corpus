from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from corpus.decorators import module_enabled

# Create your views here.


@login_required
@module_enabled(module_name="embedathon")
def index(request):
    args = {}
    return render(request, "embedathon/index.html", args)
