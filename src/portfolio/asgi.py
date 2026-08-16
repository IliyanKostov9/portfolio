"""
ASGI config for portfolio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

from portfolio.configure import configure

configure()

from configurations.asgi import get_asgi_application  # noqa: E402

application = get_asgi_application()
