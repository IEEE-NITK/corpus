from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, "events/dashboard.html")

def create_event(request):
    return render(request, "events/create_event.html")

def manage_event(request):
    return render(request, "events/manage_event.html")

def report(request):
    return render(request, "events/report.html")
