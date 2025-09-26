import os
from typing import Any

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import View

from portfolio.helpers.client import get_client_ip
from portfolio.helpers.email import Email
from portfolio.monitor.log import logger
from apps.landing_page.forms.contact_me_form import ContactMe, ContactMeForm


class ContactMeView(View):
    LOG = logger.bind(module="contact_me_view")

    def post(self, request: Any) -> HttpResponse:
        client_ip: str = get_client_ip(request)

        self.LOG.info(
            f"User: {client_ip} is requesting to send an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
            code=200,
        )

        form: ContactMeForm = ContactMeForm(request.POST)

        if form.is_valid():
            contact_me: ContactMe = ContactMe.from_form(form)

            try:
                Email.send(
                    subject=f"{contact_me.email} contacted you from your portfolio 'ContactMe'",
                    message=f"Name: {contact_me.name}\n\n" + contact_me.message,
                    recipient=os.environ.get("PORTFOLIO_TO_EMAIL"),
                )
                messages.success(
                    request,
                    "You have successfully sent an email to Iliyan!",
                )
                self.LOG.success(
                    f"User: {client_ip} has successfully sent an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
                    code=200,
                )

            except ValueError as error:
                self.LOG.error(
                    f"Application error: Cannot send an email,{error} .Aborting email send request from user {client_ip}",
                    code=500,
                )
                messages.error(
                    request,
                    "Error in sending your email message. Please try again next time :(",
                )

            return redirect("home")
        else:
            print("Form is invalid for some reason!")
            self.LOG.error(
                f"User: {client_ip} cannot send an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}, because of an invalid data he put on the form",
                code=400,
            )

            return HttpResponseBadRequest()
