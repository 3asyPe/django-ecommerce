from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url

from typing import Union

from carts.services import update_cart_part_of_session_data
from .models import GuestEmail


def update_session_data(request):
    update_cart_part_of_session_data(request)


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


def _delete_guest_email_key(request):
    try:
        del request.session["guest_email"]
    except:
        pass
