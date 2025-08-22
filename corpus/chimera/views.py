from django.shortcuts import render

# Create your views here.
def project_chimera_home(request):
    return render(request, "chimera/home.html")
