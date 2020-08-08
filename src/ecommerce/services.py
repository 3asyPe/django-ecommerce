from carts.services import update_cart_part_of_session_data


def update_session_data(request):
    update_cart_part_of_session_data(request)
