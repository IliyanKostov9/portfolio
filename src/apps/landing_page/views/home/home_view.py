from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View
from landing_page.models.education import Education
from landing_page.models.technology import Technology
from landing_page.models.work_history import WorkHistory


class HomeView(View):
    def get(self, request: Any) -> HttpResponse:
        template = loader.get_template("pages/home/index.html")

        technologies = Technology().transform()
        work_histories = WorkHistory().transform()
        educations = Education().transform()

        context: dict[str, Any] = {
            "technologies": technologies,
            "work_histories": work_histories,
            "educations": educations,
        }

        return HttpResponse(template.render(context, request))
