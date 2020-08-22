from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url

from typing import Union

from ecommerce.services import update_session_data
from .models import GuestEmail


def custom_login(request, username: str, password: str) -> bool:
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request=request, user=user)
        _delete_guest_email_key(request)
        update_session_data(request)
        print("\n\n custom login")
        return True
    return False


def get_next_path(request, base_url='/') -> str:
    next_ = request.GET.get('next')
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None
    print(f"is save {is_safe_url(redirect_path, request.get_host())}")
    if is_safe_url(redirect_path, request.get_host()):
        return redirect_path
    else:
        return base_url


def get_or_create_guest_email(request, email=None) -> Union[GuestEmail, None]:
    email = request.session.get("guest_email") if email is None else email
    print("get_guest_email")
    if email is None:
        return None
    guest_email, guest_email_created = GuestEmail.objects.get_or_create(email=email)
    request.session["guest_email"] = guest_email.email
    return guest_email


def _delete_guest_email_key(request):
    try:
        del request.session["guest_email"]
    except:
        pass
