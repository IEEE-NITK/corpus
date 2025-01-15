from django.shortcuts import render


def diodexcelerate_view(request):
    return render(request, "diodexcelerate/home.html")
