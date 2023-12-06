import random


def create_otp_code(length=5):  # create a random digit number
    return str(random.randint((10 ** (length - 1)), (10**length - 1)))


def get_client_ip(request):
    # Attempt to get the real client IP address, considering proxies and load balancers
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
