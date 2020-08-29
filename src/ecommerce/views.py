from django.http import HttpResponse, JsonResponse
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
    print("\n\ncontact_page")
    context = {
        "title": "Contact",
        "content": "Welcome to the contact page",
        "form": form,
    }
    if form.is_valid():
        print(f"cleaned data-{form.cleaned_data}")
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission!"})
        
    if form.errors:
        errors = form.errors.as_json()
        print(f"errors-{errors}")
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type="application/json")
        
    return render(request, "contact/view.html", context)
