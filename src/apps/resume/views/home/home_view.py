from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View

from apps.resume.models.certification import Certification
from apps.resume.models.education import Education
from apps.resume.models.project import Project
from apps.resume.models.technology import Technology
from apps.resume.models.work_history import WorkHistory
from apps.resume.models.language import Language
from portfolio.monitor.log import logger


class HomeView(View):
    LOG = logger.bind(module="home_view")

    def get(self, request: Any) -> HttpResponse:
        self.LOG.info(
            f"User: {request.META.get('REMOTE_ADDR')} is requesting to view the resume page",
            code=200,
        )

        template = loader.get_template("pages/home/index.html")

        technologies = Technology().transform()
        work_histories = WorkHistory().transform()
        educations = Education().transform()
        certifications = Certification().transform()
        projects = Project().transform()
        languages = Language().transform()

        context: dict[str, Any] = {
            "technologies": technologies,
            "work_histories": work_histories,
            "educations": educations,
            "certificates": certifications,
            "projects": projects,
            "languages": languages,
        }

        self.LOG.success(
            f"Page load for home view was successfull for user {request.META.get('REMOTE_ADDR')}",
            code=200,
        )
        return HttpResponse(template.render(context, request))
