from django.shortcuts import render

# Create your views here.

def landing(request):
    return render(request,"tlm/landing.html", {
        "event_date": "2026-03-24T23:59:59"
    })