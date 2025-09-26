from django.http import HttpResponse
from typing import Any
import os

from portfolio.helpers.email import Email
from django.views import View

from portfolio.helpers.client import get_client_ip
from portfolio.monitor.log import logger


class CSPReportView(View):
    LOG = logger.bind(module="csp_report_view")

    def post(self, request: Any) -> HttpResponse:
        client_ip: str = get_client_ip(request)
        stringified_request = self._stringify_request(request)

        message: str = f"""
            Content Security Policy has been violated by client: {client_ip}
            Full details: {stringified_request}
            """

        self.LOG.info(
            message,
            code=200,
        )

        if os.environ.get("PORTFOLIO_ENV") != "dev":
            try:
                Email.send(
                    subject="CSP has been violated",
                    message=message,
                    recipient=os.environ.get("PORTFOLIO_TO_EMAIL"),
                )
            except ValueError as error:
                self.LOG.error(
                    f"Cannot send CSP violation for user {client_ip}, error: {error}",
                    code=500,
                )

        return HttpResponse("Report send!")

    def _stringify_request(self, request: Any) -> str:
        return request.body.decode("utf-8").replace("{", "{{").replace("}", "}}")
