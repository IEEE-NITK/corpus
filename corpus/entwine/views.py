from django.shortcuts import render


def entwine_view(request):
    return render(request, "entwine/home.html")
