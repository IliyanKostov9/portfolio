from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.landing_page.data_class.portfolio.portfolio import Portfolio


@dataclass(frozen=True)
class Language(Portfolio):
    name: str
    proficiency: str
    flag: bool
    row: int

    @classmethod
    def from_yaml(cls, path: str) -> list["Language"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        language_model = apps.get_model(Portfolio.app_name, "Language")
        language_model.objects.all().delete()

        languages: list[Language] = Language.from_yaml("portfolio/language.yaml")

        for language in languages:
            language_model.objects.create(
                name=language.name,
                proficiency=language.proficiency,
                row=language.row,
                flag=language.flag,
            )
