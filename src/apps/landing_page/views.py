from typing import Any, Final
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods  # require_POST

APP_NAME: Final[str] = "landing_page"


@require_http_methods(["GET"])
def home(request: Any) -> HttpResponse:
    template = loader.get_template(f"{APP_NAME}/home.html")
    return HttpResponse(template.render({}, request))
