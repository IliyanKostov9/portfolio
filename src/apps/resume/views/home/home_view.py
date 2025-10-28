import os
from typing import Any

import yaml
from django.http import HttpResponse
from django.template import loader
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django.views import View

from apps.resume.models.certification import Certification
from apps.resume.models.education import Education
from apps.resume.models.language import Language
from apps.resume.models.project import Project
from apps.resume.models.technology import Technology
from apps.resume.models.work_history import WorkHistory
from portfolio.monitor.log import logger


class HomeView(View):
    LOG = logger.bind(module="home_view")

    def get(self, request: Any) -> HttpResponse:
        self.LOG.info(
            f"User: {request.META.get('REMOTE_ADDR')} is requesting to view the resume page",
            code=200,
        )

        content = self._read_yaml("page_content.yaml")

        template = loader.get_template("pages/home/index.html")

        technologies = Technology().transform()
        work_histories = WorkHistory().transform()
        educations = Education().transform()
        certifications = Certification().transform()
        projects = Project().transform()
        languages = Language().transform()

        text = self._translate(content["body"]["about"])

        print("This is test> " + str(text))

        context: dict[str, Any] = {
            "headers": self._translate(content["headers"]),
            "tr_main": self._translate(content["body"]["main"]),
            "tr_about": self._translate(content["body"]["about"]),
            "language": get_language(),
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

    def _read_yaml(self, file_name: str) -> Any:
        if not file_name.endswith((".yaml", ".yml")):
            raise InterruptedError("File must end with yml or yaml!")

        parent_dir: str = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "config")
        )

        with open(os.path.join(parent_dir, file_name), "r") as file:
            return yaml.safe_load(file)

    def _translate(self, obj) -> Any:
        if isinstance(obj, str):
            return _(obj)
        elif isinstance(obj, list):
            return [self._translate(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: self._translate(v) for k, v in obj.items()}
        return obj
