from typing import Final
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods, require_POST

APP_NAME: Final[str] = "landing_page"


@require_http_methods(["GET"])
def home(request):
    template = loader.get_template(f"{APP_NAME}/home.html")
    return HttpResponse(template.render({}, request))


@require_http_methods(["GET"])
def projects():
    return HttpResponse("Projects")


@require_POST
def contact():
    return HttpResponse("Contact")


@require_http_methods(["GET"])
def about():
    return HttpResponse("About")
