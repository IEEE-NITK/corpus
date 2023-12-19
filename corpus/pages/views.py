from config.models import SIG
from config.models import Society
from django.shortcuts import redirect
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


def sig(request, sig_name):
    try:
        sig = SIG.objects.get(name=sig_name)
    except SIG.DoesNotExist:
        return redirect("index")
    return render(
        request,
        "pages/sig.html",
        {
            "sig": sig,
        },
    )
