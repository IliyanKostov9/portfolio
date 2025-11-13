from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.resume.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class Education(Portfolio):
    en_degree: str
    bg_degree: str
    fr_degree: str
    ge_degree: str

    en_specialty: str
    bg_specialty: str
    fr_specialty: str
    ge_specialty: str

    en_university_name: str
    bg_university_name: str
    fr_university_name: str
    ge_university_name: str

    en_description: str
    bg_description: str
    fr_description: str
    ge_description: str

    scroll_description: bool
    image: str
    href_tooltip: str

    en_href_title: str
    bg_href_title: str
    fr_href_title: str
    ge_href_title: str

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
        translation_model = apps.get_model(Portfolio.app_name, "Translation")

        education_model.objects.all().delete()

        for education in Education.from_yaml("education.yaml"):
            for lang in Portfolio.languages:
                education_model.objects.create(
                    degree=getattr(education, lang + "_degree"),
                    specialty=getattr(education, lang + "_specialty"),
                    university_name=getattr(education, lang + "_university_name"),
                    description=getattr(education, lang + "_description"),
                    scroll_description=education.scroll_description,
                    image=education.image,
                    href_tooltip=education.href_tooltip,
                    href_title=getattr(education, lang + "_href_title"),
                    date=education.date,
                    gpa=education.gpa,
                    language=translation_model.objects.get(language=lang),
                )
