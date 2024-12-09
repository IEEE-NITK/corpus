from django.shortcuts import render
from corpus.decorators import module_enabled
# Create your views here.

@module_enabled(module_name="newsletter")
def home(request):
    return render(request, 'newsletter/home.html')
