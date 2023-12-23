from config.models import SIG
from config.models import Society
from django.shortcuts import get_object_or_404
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


def sig(request, sig_slug):
    sig_data = get_object_or_404(SIG, slug=sig_slug)

    # Retrieve the related society details using the SIG instance
    societies_linked_to_sig = sig_data.societies.all()

    return render(
        request,
        "pages/sig.html",
        {
            "sig": sig_data,
            "societies_linked_to_sig": societies_linked_to_sig,
        },
    )
