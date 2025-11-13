from typing import Any

from django.db.models import CASCADE, BooleanField, CharField, ForeignKey
from django.forms.models import model_to_dict
from django.utils.translation import get_language
from typing_extensions import override

from apps.resume.models.portfolio import Portfolio
from apps.resume.models.translation import Translation


class Education(Portfolio):
    degree: CharField = CharField("Degree name", max_length=100)
    specialty: CharField = CharField("Specialty name", max_length=100)
    university_name: CharField = CharField("University name", max_length=50)
    description: CharField = CharField("Description of the education", max_length=300)
    scroll_description: BooleanField = BooleanField(
        "Whether or not the description should be scrollable or not", default=False
    )
    image: CharField = CharField("Image of the education", max_length=30)
    href_tooltip: CharField = CharField("Href tooltip of the education", max_length=30)
    href_title: CharField = CharField("Href title of the education", max_length=200)
    date: CharField = CharField("Date of the education")
    gpa: CharField = CharField("GPA of the education")

    language: ForeignKey = ForeignKey(
        Translation,
        verbose_name="Translated education info",
        on_delete=CASCADE,
    )

    @override
    def get_all(self) -> Any:
        return list(Education.objects.filter(language=get_language()))

    @override
    def transform(self) -> Any:
        education_objs = [model_to_dict(wh) for wh in self.get_all()]

        return education_objs

    @override
    def clean(self, education_objs: list[Any]) -> None:
        for education in education_objs:
            education.pop("id")
