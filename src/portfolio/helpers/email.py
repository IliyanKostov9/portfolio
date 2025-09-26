import os

from django.core.mail import EmailMessage


class Email:
    @staticmethod
    def send(subject: str, message: str, recipient: str) -> None | ValueError:
        mandatory_env_variables: list[str] = [
            "PORTFOLIO_FROM_EMAIL",
            "PORTFOLIO_TO_EMAIL",
            "PORTFOLIO_EMAIL_HOST",
            "PORTFOLIO_EMAIL_USER",
            "PORTFOLIO_EMAIL_PASSWORD",
        ]

        for env_var in mandatory_env_variables:
            if not os.environ.get(env_var):
                raise ValueError(f"Environment variable {env_var} is NOT SET!")

        _ = EmailMessage(
            subject=subject,
            body=message,
            to=[recipient],
        ).send()
