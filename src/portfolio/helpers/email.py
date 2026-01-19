from django.core.mail import EmailMessage
from portfolio.helpers.utils import check_if_env_vars_are_set


class Email:
    @staticmethod
    def send(subject: str, message: str, recipient: str) -> None | ValueError:
        check_if_env_vars_are_set(
            [
                "PORTFOLIO_FROM_EMAIL",
                "PORTFOLIO_TO_EMAIL",
                "PORTFOLIO_EMAIL_HOST",
                "PORTFOLIO_EMAIL_USER",
                "PORTFOLIO_EMAIL_PASSWORD",
            ]
        )

        _ = EmailMessage(
            subject=subject,
            body=message,
            to=[recipient],
        ).send()
