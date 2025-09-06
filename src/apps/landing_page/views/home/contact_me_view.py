import os
from typing import Any

from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import View

from portfolio.monitor.log import logger
from apps.landing_page.forms.contact_me_form import ContactMe, ContactMeForm


class ContactMeView(View):
    LOG = logger.bind(module="contact_me_view")

    def post(self, request: Any) -> HttpResponse:
        self.LOG.info(
            f"User: {request.META.get('REMOTE_ADDR')} is requesting to send an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
            code=200,
        )

        form: ContactMeForm = ContactMeForm(request.POST)

        if form.is_valid():
            self._check_email_envs_are_set(request.META.get("REMOTE_ADDR"))

            contact_me: ContactMe = ContactMe.from_form(form)

            _ = EmailMessage(
                subject=f"{contact_me.email} contacted you from your portfolio 'ContactMe'",
                body=f"Name: {contact_me.name}\n\n" + contact_me.message,
                to=[os.environ.get("PORTFOLIO_TO_EMAIL")],
            ).send()

            messages.success(
                request,
                "You have successfully sent an email to Iliyan!",
            )

            self.LOG.success(
                f"User: {request.META.get('REMOTE_ADDR')} has successfully sent an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
                code=200,
            )

            return redirect("home")
        else:
            print("Form is invalid for some reason!")
            self.LOG.error(
                f"User: {request.META.get('REMOTE_ADDR')} cannot send an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}, because of an invalid data he put on the form",
                code=400,
            )

            return HttpResponseBadRequest()

    def _check_email_envs_are_set(self, user_ip_address: str) -> None:
        mandatory_env_variables: list[str] = [
            "PORTFOLIO_FROM_EMAIL",
            "PORTFOLIO_TO_EMAIL",
            "PORTFOLIO_EMAIL_HOST",
            "PORTFOLIO_EMAIL_USER",
            "PORTFOLIO_EMAIL_PASSWORD",
        ]

        for env_var in mandatory_env_variables:
            if not os.environ.get(env_var):
                self.LOG.error(
                    f"Application error: Cannot send an email, because the environment variable {env_var} is missing. Aborting email send request from user {user_ip_address}",
                    code=500,
                )
                # TODO: Redirect user to error page 500
                raise ValueError(f"Environment variable {env_var} is NOT SET!")
