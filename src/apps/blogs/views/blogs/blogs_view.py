from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View

from portfolio.helpers.client import get_client_ip
from portfolio.monitor.log import logger


class BlogsView(View):
    LOG = logger.bind(module="blogs_view")

    def get(self, request: Any) -> HttpResponse:
        self.LOG.info(
            f"User: {get_client_ip(request)} is requesting to view the blogs page",
            code=200,
        )

        template = loader.get_template("pages/blogs/index.html")

        context: dict[str, Any] = {}

        self.LOG.success(
            f"Page load for blogs view was successfull for user {get_client_ip(request)}",
            code=200,
        )
        return HttpResponse(template.render(context, request))
