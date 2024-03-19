from django.shortcuts import render
from virtual_expo.models import Report


# Create your views here.
def home(request):
    years = list(Report.objects.values_list("year", flat=True).distinct())

    args = {"years": years}

    return render(request, "virtual_expo/home.html", args)
