from django.shortcuts import render
from skyward_expedition.models import SEUser


# Create your views here.
def home(request):
    args = {}

    if request.user is not None and request.user.is_authenticated:
        se_user = SEUser.objects.filter(user=request.user).first()
        if se_user is not None:
            args["dashboard"] = True

        if request.user.groups.filter(name__in="se_admin").exists():
            args["admin"] = True

    return render(request, "skyward_expedition/home.html", args)
