from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "virtual_expo/home.html")
