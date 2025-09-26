from typing import Any


def get_client_ip(request: Any) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip: str = request.META.get("REMOTE_ADDR")
    return ip


def get_client_user_agent(request: Any) -> str:
    return request.META["HTTP_USER_AGENT"]
