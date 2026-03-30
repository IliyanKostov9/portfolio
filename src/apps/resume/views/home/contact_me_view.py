import os
from typing import Any

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views import View

from django.utils.translation import get_language
from apps.resume.forms.contact_me_form import ContactMe, ContactMeForm
from portfolio.helpers.email import Email
from portfolio.helpers.security_manager import SecurityManager
from portfolio.monitor.log import logger


class ContactMeView(View):
    LOG = logger.bind(module="contact_me_view")

    def post(self, request: Any) -> HttpResponse:
        form: ContactMeForm = ContactMeForm(request.POST)

        self.LOG.info(
            f"User is requesting to send an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
            code=200,
        )

        if form.is_valid():
            contact_me: ContactMe = ContactMe.from_form(form)

            if request.POST.get("submitContactmeBtn"):
                return self.__send_email_to_iliyan(
                    request,
                    f"{contact_me.email} contacted you from your portfolio 'ContactMe'",
                    f"Name: {contact_me.name}</br>Message: {contact_me.message}",
                    _("You have successfully sent an email to Iliyan!"),
                )
            elif request.POST.get("submitCVDownloadBtn"):
                token: str = SecurityManager.generate_token(
                    os.environ.get("PORTFOLIO_TO_EMAIL")
                )

                http_protocol: str = (
                    "https" if os.environ.get("SECURE_SSL_REDIRECT") else "http"
                )

                host: str = os.environ.get("PORTFOLIO_HOST")
                if host == "localhost":
                    host += ":8000"

                url_yes: str = (
                    f"{http_protocol}://{host}/home/cv-download/{token}/?choice=yes&email={contact_me.email}&language={get_language()}"
                )
                url_no: str = (
                    f"{http_protocol}://{host}/home/cv-download/{token}/?choice=no&email={contact_me.email}&language={get_language()}"
                )

                Email.send(
                    subject=_("Thanks for contacting Iliyan!"),
                    message=_(
                        "We've contacted Iliyan with your request to download his CV. Please make sure to watch your email box for the status of this request\n\nThanks and have a nice day!"
                    ),
                    recipient=contact_me.email,
                )

                return self.__send_email_to_iliyan(
                    request,
                    f"{contact_me.email} has made a request to download your CV",
                    f"Name: {contact_me.name}</br>Message: {contact_me.message}</br></br>Accept/Refuse: (<a href='{url_yes}'>Yes</a>/<a href='{url_no}'>No</a>)",
                    _(
                        "You have successfully sent a CV download request to Iliyan!\n Please wait for him to either accept/refuse your request.\n\nPlease make sure to look at your junk folder, that's where the email may end up in.\nWe'll make sure to update you regarding the status in your email box :)"
                    ),
                )
            else:
                self.LOG.error(
                    "Unrecognized POST request: Incorrect button id!",
                    code=400,
                )
                messages.error(
                    request,
                    _("Application error! Sorry for the inconvenience!"),
                )

        else:
            self.LOG.error(
                f"User cannot send an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}, because of invalid data he put on the form",
                code=400,
            )

            return HttpResponseBadRequest()

    def __send_email_to_iliyan(
        self, request: Any, subject: str, message: str, success_message: str
    ) -> HttpResponse:
        try:
            Email.send(
                subject=subject,
                message=message,
                recipient=os.environ.get("PORTFOLIO_TO_EMAIL"),
                send_as_html=True,
            )

            self.LOG.success(
                f"User has successfully sent an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
                code=200,
            )
            messages.success(request, success_message)

        except ValueError as error:
            self.LOG.error(
                f"Application error: Cannot send an email,{error}. Aborting email send...",
                code=500,
            )
            messages.error(
                request,
                _("Error in sending your email message. Please try again next time :("),
            )

        return redirect("home")
