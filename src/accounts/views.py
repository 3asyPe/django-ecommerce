from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm, GuestForm
from .services import (
    custom_login,
    get_next_path,
)
from .models import GuestEmail


User = get_user_model()


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        email = form.cleaned_data.get("email")
        GuestEmail.objects.new_or_get(request, email=email)
        path = get_next_path(request)
        return redirect(path)

    return redirect("/register/")


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        logged_in = custom_login(request, username=username, password=password)
        if logged_in:
            path = get_next_path(request)
            return redirect(path)
        else:
            # TODO show an error
            print("error")

    return render(request, "accounts/login.html", context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        user = form.save()
        if user:
            return redirect("/login/")
    
    return render(request, "accounts/register.html", context)
