import os
from typing import Any, Final
from io import BytesIO
from django.http import FileResponse
from django.views import View

from portfolio.helpers.email import Email
from django.utils.translation import get_language
from portfolio.monitor.log import logger
from portfolio.models.s3 import S3
from botocore.exceptions import ClientError


class CVDownloadView(View):
    LOG = logger.bind(module="cv_download_view")

    def post(self, request: Any) -> None:
        CV_S3_KEY_PATH: Final[str] = f"portfolio/cv-{get_language()}/main.pdf"

        is_user_iliyan: bool = True
        username: str = "None"
        user_email: str = "None"
        s3 = S3()
        print(username)

        try:
            if is_user_iliyan:
                try:
                    file_obj = BytesIO(s3.download(CV_S3_KEY_PATH))

                    response = FileResponse(
                        file_obj,
                        as_attachment=True,
                        filename="Iliyan_Kostov.pdf",
                        content_type="application/pdf",
                    )
                    print(response)

                    self.LOG.success(
                        f"I have successfully downloaded a file: {CV_S3_KEY_PATH}",
                        code=200,
                    )

                    Email.send(
                        subject=os.environ.get("PORTFOLIO_TO_EMAIL")
                        + " has accepted to share his CV to you!",
                        message="Good news! Iliyan agreed to have shared his CV to you!",
                        recipient=user_email,
                    )

                except ClientError as error:
                    self.LOG.error(
                        f"Application error: Cannot download a file {CV_S3_KEY_PATH} with error: {error} .Aborting downloading",
                        code=500,
                    )
            else:
                Email.send(
                    subject=os.environ.get("PORTFOLIO_TO_EMAIL")
                    + " has refused to share his CV to you",
                    message="Iliyan has refused to share his email address to you. Sorry :(",
                    recipient=user_email,
                )

            self.LOG.success(
                f"Email has been successfully send to: {os.environ.get('PORTFOLIO_TO_EMAIL')}!",
                code=200,
            )
        except ValueError as error:
            self.LOG.error(
                f"Application error: Cannot send an email,{error}. Aborting email...",
                code=500,
            )
