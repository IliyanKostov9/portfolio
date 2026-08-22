import os
from typing import Final

from configurations import Configuration

from .common import Common

ADMIN: Final[str] = "Iliyan"


class Prod(Common, Configuration):
    DEBUG = False
    CONTENT_SECURITY_POLICY = Common.CSP_POLICY
    ADMINS = [(ADMIN, os.environ.get("PORTFOLIO_TO_EMAIL"))]
    MANAGERS = [(ADMIN, os.environ.get("PORTFOLIO_TO_EMAIL"))]
    SERVER_EMAIL = os.environ.get("PORTFOLIO_FROM_EMAIL")

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600  # TODO: Increase it ?
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    CONN_MAX_AGE = None
    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = True
    STATIC_ROOT = "/var/www/portfolio.ikostov.org/static/"
    COMPRESS_ROOT = STATIC_ROOT
    COMPRESS_OUTPUT_DIR = "CACHE"

    INSTALLED_APPS = Common.apps[: len(Common.apps) - 3]
