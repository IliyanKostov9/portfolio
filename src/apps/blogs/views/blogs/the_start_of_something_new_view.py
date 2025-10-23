from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View

from portfolio.helpers.client import get_client_ip
from portfolio.monitor.log import logger


class TheStartOfSomethingNewView(View):
    LOG = logger.bind(module="the_start_of_something_new_view")

    def get(self, request: Any) -> HttpResponse:
        self.LOG.info(
            f"User: {get_client_ip(request)} is requesting to view the blogs page",
            code=200,
        )

        template = loader.get_template("pages/blogs/the_start_of_something_new.html")

        self.LOG.success(
            f"Page load for the_start_of_something_new view was successful for user {get_client_ip(request)}",
            code=200,
        )
        return HttpResponse(template.render({}, request))
