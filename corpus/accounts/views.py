from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CorpusCreationForm, CorpusLoginForm

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = CorpusCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have been successfully registered. Please sign in!")
            return redirect("accounts_signin")
    else:
        form = CorpusCreationForm()
    args = {
        "form": form
    }
    return render(request, "accounts/signup.html", args)

def signin(request):
    if request.method == "POST":
        form = CorpusLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back to Corpus!")
            return redirect("index")
    else:
        form = CorpusLoginForm()

    args = {
        "form": form
    }
    return render(request, "accounts/login.html", args)

def signout(request):
    logout(request)
    messages.success(request, "Successfully signed out.")
    return redirect("index")