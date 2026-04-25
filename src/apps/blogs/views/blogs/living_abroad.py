from typing import Any, Final

from django.http import HttpResponse
from django.template import loader
from django.views import View

from portfolio.helpers.client import get_client_ip
from portfolio.monitor.log import logger

PAGE_NAME: Final[str] = "living_abroad"


class LivingAbroadView(View):
    LOG = logger.bind(module=PAGE_NAME)

    def get(self, request: Any) -> HttpResponse:
        self.LOG.info(
            f"User: {get_client_ip(request)} is requesting to view the blogs page",
            code=200,
        )

        template = loader.get_template(f"pages/blogs/{PAGE_NAME}.html")

        self.LOG.success(
            f"Page load for {PAGE_NAME} view was successful for user {get_client_ip(request)}",
            code=200,
        )
        return HttpResponse(template.render({}, request))
