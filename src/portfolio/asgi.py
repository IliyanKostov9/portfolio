"""
ASGI config for portfolio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import mimetypes

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio.settings")

if os.environ.get("PORTFOLIO_ENV") == "dev":
    from dotenv import load_dotenv

    load_dotenv()


mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("application/javascript", ".js", True)

application = get_asgi_application()
