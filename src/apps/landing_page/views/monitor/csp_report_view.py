import os
from typing import Any

from django.views import View

from portfolio.monitor.log import logger


class CSPReportView(View):
    LOG = logger.bind(module="csp_report_view")

    def post(self, request: Any) -> None:
        self.LOG.info(
            "Content Security Policy has been violated!",
            code=200,
        )

        self.LOG.success(
            f"User: {request.META.get('REMOTE_ADDR')} has successfully sent an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
            code=200,
        )
