import os
from typing import Any, Final
from io import BytesIO
from django.contrib import messages
from django.http import FileResponse, HttpResponseBadRequest
from django.utils.translation import gettext as _
from django.views import View

from portfolio.helpers.client import get_client_ip
from portfolio.monitor.log import logger
from portfolio.models.s3 import S3
from botocore.exceptions import ClientError


class CVDownloadView(View):
    CV_S3_KEY_PATH: Final[str] = "portfolio/cv/main.pdf"
    LOG = logger.bind(module="cv_download_view")

    def get(self, request: Any) -> FileResponse | HttpResponseBadRequest:
        client_ip: str = get_client_ip(request)

        self.LOG.info(
            f"User: {client_ip} is requesting to download cv {os.environ.get('PORTFOLIO_TO_EMAIL')}",
            code=200,
        )

        s3 = S3()
        try:
            file_obj = BytesIO(s3.download(self.CV_S3_KEY_PATH))

            messages.success(
                request,
                _("You have successfully sent an email to Iliyan!"),
            )
            self.LOG.success(
                f"User: {client_ip} has successfully downloaded a file: {self.CV_S3_KEY_PATH}",
                code=200,
            )

            return FileResponse(
                file_obj,
                as_attachment=True,
                filename="Iliyan_Kostov.pdf",
                content_type="application/pdf",
            )

        except ClientError as error:
            self.LOG.error(
                f"Application error: Cannot download a file {self.CV_S3_KEY_PATH} with error: {error} .Aborting downloading for user: {client_ip}",
                code=500,
            )
            messages.error(
                request,
                _("Error in downloading Iliyan's CV. Please try again next time :("),
            )
            return HttpResponseBadRequest()
