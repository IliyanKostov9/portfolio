from typing import Any

from django.db.models import BooleanField, CharField
from typing_extensions import override

from apps.landing_page.models.portfolio import Portfolio


class Education(Portfolio):
    degree: CharField = CharField("Degree name", max_length=100)
    specialty: CharField = CharField("Specialty name", max_length=100)
    university_name: CharField = CharField("University name", max_length=50)
    description: CharField = CharField("Description of the education", max_length=300)
    scroll_description: BooleanField = BooleanField(
        "Whether or not the description should be scrollable or not"
    )
    image: CharField = CharField("Image of the education", max_length=30)
    href_tooltip: CharField = CharField("Href tooltip of the education", max_length=30)
    href_title: CharField = CharField("Href title of the education", max_length=200)
    date: CharField = CharField("Date of the education")
    gpa: CharField = CharField("GPA of the education")

    @override
    def get_all(self) -> Any:
        return list(Education.objects.all().values())

    @override
    def transform(self) -> Any:
        education_objs = self.get_all()

        self.clean(education_objs)
        return education_objs

    @override
    def clean(self, education_objs: list[Any]) -> None:
        for education in education_objs:
            education.pop("id")
