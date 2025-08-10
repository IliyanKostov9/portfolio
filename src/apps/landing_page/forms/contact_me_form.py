from dataclasses import dataclass

from django.forms import Form, Textarea
from django.forms.fields import CharField, EmailField
from typing_extensions import override


class ContactMeForm(Form):
    name: CharField = CharField(label="Name of the user", max_length=50)
    email: EmailField = EmailField(label="Email of the user")
    message: CharField = CharField(label="Message for me", widget=Textarea)


@dataclass
class ContactMe:
    name: str
    email: str
    message: str

    @classmethod
    def from_form(cls, form: Form) -> "ContactMe":
        return cls(**form.cleaned_data)

    @override
    def __str__(self) -> str:
        return f"Contact me: \n Name: {self.name}\n Email: {self.email}\n Message: {self.message}"
