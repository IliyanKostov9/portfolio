import os
from typing import Any

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views import View

from apps.resume.forms.contact_me_form import ContactMe, ContactMeForm
from portfolio.helpers.email import Email
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
                return self.__send_email_to_iliyan(contact_me, request)
            elif request.POST.get("submitCVDownloadBtn"):
                self.__send_cv_download_request_email_to_iliyan(contact_me, request)
        else:
            self.LOG.error(
                f"User cannot send an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}, because of an invalid data he put on the form",
                code=400,
            )

            return HttpResponseBadRequest()

    def __send_email_to_iliyan(
        self,
        request,
        contact_me: ContactMe,
        success_message: str = "You have successfully sent an email to Iliyan!",
    ) -> HttpResponse:
        try:
            Email.send(
                subject=f"{contact_me.email} contacted you from your portfolio 'ContactMe'",
                message=f"Name: {contact_me.name}\n\n" + contact_me.message,
                recipient=os.environ.get("PORTFOLIO_TO_EMAIL"),
            )

            self.LOG.success(
                f"User has successfully sent an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
                code=200,
            )
            messages.success(request, success_message)

        except ValueError as error:
            self.LOG.error(
                f"Application error: Cannot send an email,{error}. Aborting email send",
                code=500,
            )
            messages.error(
                request,
                _("Error in sending your email message. Please try again next time :("),
            )

        return redirect("home")

    def __send_cv_download_request_email_to_iliyan(
        self, request, contact_me: ContactMe
    ) -> None:
        self.__send_email_to_iliyan(
            request,
            contact_me,
            "You have successfully sent a CV download request to Iliyan!\n Please wait for him to either accept/refuse your request. We'll make sure to update you regarding the status in your email box :)",
        )
        self.LOG.success(
            f"User has successfully sent an email to {os.environ.get('PORTFOLIO_TO_EMAIL')}",
            code=200,
        )
        messages.success(
            request,
            _("You have successfully sent an email to Iliyan!"),
        )
