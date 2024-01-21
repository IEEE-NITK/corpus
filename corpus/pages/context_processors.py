from django.conf import settings


def tailwind_cdn_link(request):
    return {
        "USE_TAILWIND_CDN_LINK": settings.USE_TAILWIND_CDN_LINK,
    }
