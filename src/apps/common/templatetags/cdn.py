from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def cdn(path):
    return f"{settings.CDN_URL.rstrip('/')}/{path.lstrip('/')}"
