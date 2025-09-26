from django.http import HttpResponse
import json
from typing import Any

from django.views import View

from portfolio.helpers.client import get_client_ip
from portfolio.monitor.log import logger


class CSPReportView(View):
    LOG = logger.bind(module="csp_report_view")

    def post(self, request: Any) -> None:
        client_ip: str = get_client_ip(request)

        self.LOG.info(
            f"Content Security Policy has been violated by client: {client_ip}",
            code=200,
        )
        print(f">>>>>>>>>> {json.loads(request.body)}")

        # self.LOG.success(
        #     f"User: {request.META.get('REMOTE_ADDR')} has successfully sent an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
        #     code=200,
        # )

        return HttpResponse("Report send!")
