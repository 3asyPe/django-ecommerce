from .signals import object_viewed_signal


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", None)
    return ip


def send_object_viewed_data_to_analytics(instance, request):
    object_viewed_signal.send(instance.__class__, instance=instance, request=request)
