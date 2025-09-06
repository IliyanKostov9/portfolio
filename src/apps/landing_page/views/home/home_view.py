from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View

from apps.landing_page.models.certification import Certification
from apps.landing_page.models.education import Education
from apps.landing_page.models.project import Project
from apps.landing_page.models.technology import Technology
from apps.landing_page.models.work_history import WorkHistory
from portfolio.monitor.log import logger


class HomeView(View):
    LOG = logger.bind(module="home_view")

    def get(self, request: Any) -> HttpResponse:
        self.LOG.info(
            f"User: {request.META.get('REMOTE_ADDR')} is requesting to view the landing page",
            code=200,
        )

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

        self.LOG.success(
            f"Page load for home view was successfull for user {request.META.get('REMOTE_ADDR')}",
            code=200,
        )
        return HttpResponse(template.render(context, request))
