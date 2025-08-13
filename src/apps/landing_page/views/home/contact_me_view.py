import os
from typing import Any

from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from landing_page.forms.contact_me_form import ContactMe, ContactMeForm


class ContactMeView(View):
    def post(self, request: Any) -> HttpResponse:
        form: ContactMeForm = ContactMeForm(request.POST)

        if form.is_valid():
            self._check_email_envs_are_set()

            contact_me: ContactMe = ContactMe.from_form(form)
            print(contact_me)

            _ = EmailMessage(
                subject=f"{contact_me.email} contacted you from your portfolio 'ContactMe'",
                body=f"Name: {contact_me.name}\n\n" + contact_me.message,
                to=[os.environ.get("TO_EMAIL")],
            ).send()

            messages.success(
                request,
                "You have successfully sent an email to Iliyan!",
            )

            return redirect("home")
        else:
            print("Form is invalid for some reason!")
            return None

    def _check_email_envs_are_set(self) -> None:
        mandatory_env_variables: list[str] = [
            "FROM_EMAIL",
            "TO_EMAIL",
            "EMAIL_HOST",
            "EMAIL_USER",
            "EMAIL_PASSWORD",
        ]

        for env_var in mandatory_env_variables:
            if not os.environ.get(env_var):
                # TODO: Redirect user to error page 500
                raise ValueError(f"Environment variable {env_var} is NOT SET!")
