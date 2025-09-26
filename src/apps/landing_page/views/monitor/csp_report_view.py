from django.http import HttpResponse, HttpResponseBadRequest
from typing import Any
import os

from django.utils.decorators import method_decorator


from portfolio.helpers.email import Email
from django.views import View

from portfolio.helpers.client import get_client_ip, get_client_user_agent
from portfolio.monitor.log import logger
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class CSPReportView(View):
    LOG = logger.bind(module="csp_report_view")

    def post(self, request: Any) -> HttpResponse:
        client_ip: str = get_client_ip(request)
        client_user_agent: str = get_client_user_agent(request)
        stringified_request = self._stringify_request(request)

        if request.content_type not in ["application/json", "application/csp-report"]:
            self.LOG.error(
                f"Ivalid content type made by client: {client_ip} with user agent: {client_user_agent}",
                code=200,
            )
            return HttpResponseBadRequest("Invalid content type")

        message: str = f"""
            Content Security Policy has been violated by client: {client_ip} with user agent {client_user_agent}
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
