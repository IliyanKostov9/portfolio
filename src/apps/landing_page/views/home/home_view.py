from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View


class HomeView(View):
    def get(self, request: Any, *args, **kwargs) -> HttpResponse:
        template = loader.get_template("home.html")

        return HttpResponse(template.render({}, request))
