def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # None is written to handle Errors
        # If In case unable to get the client's IP address
        ip = request.META.get('REMOTE_ADDR', None)
    return ip
