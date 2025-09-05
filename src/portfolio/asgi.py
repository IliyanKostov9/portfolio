"""
ASGI config for portfolio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")

if os.environ.get("PORTFOLIO_ENV") == "dev":
    from dotenv import load_dotenv

    load_dotenv()

if os.environ.get("PORTFOLIO_ENV") == "prod":
    application = get_asgi_application()
else:
    application = WhiteNoise(
        get_asgi_application(), root="/var/www/portfolio.ikostov.org/static"
    )
