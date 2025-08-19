from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.landing_page.data_class.portfolio.portfolio import Portfolio


@dataclass(frozen=True)
class Education(Portfolio):
    degree: str
    specialty: str
    university_name: str
    description: str
    scroll_description: bool
    image: str
    href_tooltip: str
    href_title: str
    date: str
    gpa: str

    @classmethod
    def from_yaml(cls, path: str) -> list["Education"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        education_model = apps.get_model(Portfolio.app_name, "Education")
        education_model.objects.all().delete()

        educations: list[Education] = Education.from_yaml("portfolio/education.yaml")

        for education in educations:
            education_model.objects.create(
                degree=education.degree,
                specialty=education.specialty,
                university_name=education.university_name,
                description=education.description,
                scroll_description=education.scroll_description,
                image=education.image,
                href_tooltip=education.href_tooltip,
                href_title=education.href_title,
                date=education.date,
                gpa=education.gpa,
            )
