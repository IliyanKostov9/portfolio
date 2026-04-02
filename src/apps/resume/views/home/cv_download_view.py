import os
from typing import Any, Final
from io import BytesIO
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.views import View

from django.utils.translation import gettext as _, override
from portfolio.helpers.email import Email
from portfolio.helpers.security_manager import SecurityManager
from portfolio.monitor.log import logger
from portfolio.models.aws.s3 import S3
from botocore.exceptions import ClientError


class CVDownloadView(View):
    LOG = logger.bind(module="cv_download_view")

    def get(
        self, request: Any, token: str
    ) -> HttpResponse | HttpResponseForbidden | HttpResponseServerError:
        s3 = S3()

        is_user_iliyan: bool = SecurityManager.verify_token(token)
        does_iliyan_want_to_share_his_cv: bool = (
            True if request.GET.get("choice") == "yes" else False
        )
        user_email: str = request.GET.get("email")

        user_language: str = request.GET.get("language", "en")
        CV_S3_KEY_PATH: Final[str] = f"portfolio/cv-{user_language}/main.pdf"

        if is_user_iliyan:
            try:
                if does_iliyan_want_to_share_his_cv:
                    file_obj = BytesIO(s3.download(CV_S3_KEY_PATH))

                    self.LOG.success(
                        f"I have successfully downloaded a file: {CV_S3_KEY_PATH}",
                        code=200,
                    )

                    with override(user_language):
                        Email.send(
                            subject=_(
                                "{email} has accepted to share his CV to you!"
                            ).format(email=os.environ.get("PORTFOLIO_TO_EMAIL")),
                            message=_(
                                "Good news! Iliyan agreed to have shared his CV to you!"
                            ),
                            recipient=user_email,
                            attachments=[
                                (
                                    "Iliyan_Kostov.pdf",
                                    file_obj.getbuffer(),
                                    "application/pdf",
                                )
                            ],
                        )
                else:
                    with override(user_language):
                        Email.send(
                            subject=_(
                                "{email} has refused to share his CV to you"
                            ).format(email=os.environ.get("PORTFOLIO_TO_EMAIL")),
                            message=_(
                                "Iliyan has refused to share his CV to you. Sorry :("
                            ),
                            recipient=user_email,
                        )

                self.LOG.success(
                    f"Email has been successfully send to: {os.environ.get('PORTFOLIO_TO_EMAIL')}!",
                    code=200,
                )
                return HttpResponse(
                    "You have "
                    + ("sent" if does_iliyan_want_to_share_his_cv else "not sent")
                    + " your CV to user "
                    + user_email,
                    content_type="text/plain",
                )

            except ClientError as error:
                self.LOG.error(
                    f"Application error: Cannot download a file {CV_S3_KEY_PATH} with error: {error}. Aborting downloading...",
                    code=500,
                )
            except ValueError as error:
                self.LOG.error(
                    f"Application error: Cannot send an email,{error}. Aborting email...",
                    code=500,
                )

            return HttpResponseServerError()
        else:
            return HttpResponseForbidden()
