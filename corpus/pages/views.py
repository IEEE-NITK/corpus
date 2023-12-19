from config.models import SIG
from config.models import Society
from django.shortcuts import render


def index(request):
    # Get all societies to render on landing page Societies section
    societies = Society.objects.all()

    return render(
        request,
        "pages/index.html",
        {
            "societies": societies,
        },
    )


def about_us(request):
    societies = Society.objects.all()

    return render(
        request,
        "pages/about_us.html",
        {
            "socieites": societies,
        },
    )

def impulse(request):

    return render(
        request,
        "pages/impulse.html",
    )

def compsoc(request):
    sigs = SIG.objects.all()

    return render(
        request,
        "pages/sig.html",
        {
            "sigs": sigs,
        },
    )
