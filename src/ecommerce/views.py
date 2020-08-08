from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm


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
