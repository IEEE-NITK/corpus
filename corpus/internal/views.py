from django.shortcuts import render


def design_system(request):
    args = {}
    return render(request, "internal/design_system.html", args)
