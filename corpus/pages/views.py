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


def sig(request, sig_name):
    sig_data = get_object_or_404(SIG, slug=sig_name)

    # Retrieve the related society details using the SIG instance
    societies_linked_to_sig = sig_data.societies.all()

    events_linked_to_sig = sig_data.events.all().order_by('order')
    alumnilogos_linked_to_sig = sig_data.alumni_logos.all()

    args = {
        "sig": sig_data,
        "societies_linked_to_sig": societies_linked_to_sig,
        "events": events_linked_to_sig,
        "alumni_logos": alumnilogos_linked_to_sig,
    }

    return render(request, "pages/sig.html", args)



def farewell(request):
    return render(request, "pages/farewell.html")
