from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm


User = get_user_model()

def home_page(request):
    context = {
        "title": "Hello world!",
        "content": "Welcome to the homepage"
    }
    if request.user.is_authenticated:
        context['premium_content'] = "YEAAAAHHHH"
    return render(request, "home_page.html", context)


def about_page(request):
    context = {
        "title": "About Page",
        "content": "Welcome to the aboutpage",
    }
    return render(request, "home_page.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        print(request.user.is_authenticated)
        if user is not None:
            login(request, user)
            context['form'] = LoginForm()
            print(request.user.is_authenticated)
            return redirect('/')
        else:
            print("error")

    return render(request, "auth/login.html", context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = User.objects.create_user(username, email, password)
        print(user)
    
    return render(request, "auth/register.html", context)


def contact_page(request):
    form = ContactForm(request.POST or None)
    context = {
        "title": "Contact",
        "content": "Welcome to the contactpage",
        "form": form,
    }
    if form.is_valid():
        print(form.cleaned_data)
    return render(request, "contact/view.html", context)
