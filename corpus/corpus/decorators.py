from config.models import ModuleConfiguration
from django.contrib import messages
from django.shortcuts import redirect


def module_enabled(module_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            try:
                config = ModuleConfiguration.objects.get(module_name=module_name)
            except ModuleConfiguration.DoesNotExist:
                messages.error(
                    request,
                    """
                        Module Configuration does not exist.
                        Please contact the administrators!
                    """,
                )
                return redirect("index")

            if not config.module_enabled:
                messages.error(
                    request,
                    """
                        Module has not been enabled.
                        Please contact the administrators!
                    """,
                )
                return redirect("index")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def ensure_group_membership(group_names):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    """
                    Permission denied.
                    Please contact the administrators if you think there is some issue.
                    """,
                )
                return redirect("index")

        return wrapper

    return decorator
