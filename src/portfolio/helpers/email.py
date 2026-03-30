from django.core.mail import EmailMessage
from portfolio.helpers.utils import check_if_env_vars_are_set


class Email:
    @staticmethod
    def send(
        subject: str,
        message: str,
        recipient: str,
        attachments: list[str] | None = None,
        send_as_html: bool = False,
    ) -> None | ValueError:
        check_if_env_vars_are_set(
            [
                "PORTFOLIO_FROM_EMAIL",
                "PORTFOLIO_TO_EMAIL",
                "PORTFOLIO_EMAIL_HOST",
                "PORTFOLIO_EMAIL_USER",
                "PORTFOLIO_EMAIL_PASSWORD",
            ]
        )

        email = EmailMessage(
            subject=subject, body=message, to=[recipient], attachments=attachments
        )

        if send_as_html:
            email.content_subtype = "html"

        email.send()
