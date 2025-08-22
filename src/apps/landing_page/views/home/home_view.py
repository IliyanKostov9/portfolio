from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View

from apps.landing_page.models.certification import Certification
from apps.landing_page.models.education import Education
from apps.landing_page.models.project import Project
from apps.landing_page.models.technology import Technology
from apps.landing_page.models.work_history import WorkHistory


class HomeView(View):
    def get(self, request: Any) -> HttpResponse:
        template = loader.get_template("pages/home/index.html")

        technologies = Technology().transform()
        work_histories = WorkHistory().transform()
        educations = Education().transform()
        certifications = Certification().transform()
        projects = Project().transform()

        context: dict[str, Any] = {
            "technologies": technologies,
            "work_histories": work_histories,
            "educations": educations,
            "certificates": certifications,
            "projects": projects,
        }

        return HttpResponse(template.render(context, request))
