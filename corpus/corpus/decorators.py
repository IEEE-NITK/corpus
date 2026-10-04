from datetime import datetime
from functools import wraps
from zoneinfo import ZoneInfo

from accounts.models import ExecutiveMember
from config.models import ModuleConfiguration
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone


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


def ensure_exec_membership():
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            try:
                exec_member = ExecutiveMember.objects.get(user=request.user.id)
                request.exec_member = exec_member
                return view_func(request, *args, **kwargs)
            except ExecutiveMember.DoesNotExist:
                messages.error(
                    request,
                    """
                    Permission denied.
                    Please contact the administrators if you think there is an issue.
                    """,
                )
                return redirect("index")

        return wrapper

    return decorator


def ensure_view_current_envision():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            config = ModuleConfiguration.objects.get(
                module_name="virtual_expo"
            ).module_config

            try:
                ExecutiveMember.objects.get(user=request.user.id)
                exec_member = True
            except ExecutiveMember.DoesNotExist:
                exec_member = False

            can_view_current_envision = exec_member or config.get(
                "view_current_envision"
            )
            kwargs["can_view_current_envision"] = can_view_current_envision
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def event_time_gate(
    start_time,
    end_time=None,
    pre_template="tlm/403.html",
    post_template="tlm/event_ended.html",
    context=None,
):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            now = timezone.now()
            ctx = context or {}

            # Before launch
            if now < start_time:
                return render(request, pre_template, ctx, status=403)

            # After event end
            if end_time and now > end_time:
                return render(request, post_template, ctx, status=403)

            # During event
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
