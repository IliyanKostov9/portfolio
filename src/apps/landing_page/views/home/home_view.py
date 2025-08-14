from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View
from landing_page.models.technology import Technology


class HomeView(View):
    def get(self, request: Any) -> HttpResponse:
        template = loader.get_template("pages/home/index.html")
        technologies = Technology.objects.all().values()

        for technology in technologies:
            print(f"tech: {technology}")

        return HttpResponse(template.render({}, request))
