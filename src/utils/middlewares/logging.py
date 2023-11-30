from django.utils import timezone

import logging


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        response = self.get_response(request)
        self.log_api_request(request, response)
        return response

    def log_api_request(self, request, response):
        user_pk = request.user.pk if request.user.is_authenticated else "Anonymous"
        url = request.build_absolute_uri()
        headers = dict(request.headers)
        browser = request.META.get("HTTP_USER_AGENT", "N/A")
        ip_address = self.get_client_ip(request)
        location = request.META.get("REMOTE_ADDR", "N/A")

        log_message = (
            f"User: {user_pk}\n"
            f"URL: {url}\n"
            f"Headers: {headers}\n"
            f"Browser: {browser}\n"
            f"IP Address: {ip_address}\n"
        )

        if response.status_code >= 400:
            log_message += f"Response: {response.content}\n"

        # Log to file
        log_file_path = f"logs/{timezone.now().strftime('%d-%m-%Y')}.log"
        logger = logging.getLogger("api_logs")
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.info(log_message)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
