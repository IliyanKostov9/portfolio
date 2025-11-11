from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.resume.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class LanguageProficiency(Portfolio):
    en_name: str
    bg_name: str
    fr_name: str
    ge_name: str

    proficiency: str
    icon: str
    row: int

    @classmethod
    def from_yaml(cls, path: str) -> list["LanguageProficiency"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        language_model = apps.get_model(Portfolio.app_name, "LanguageProficiency")
        translation_model = apps.get_model(Portfolio.app_name, "Translation")

        language_model.objects.all().delete()

        for language in LanguageProficiency.from_yaml("language_proficiency.yaml"):
            for lang in Portfolio.languages:
                language_model.objects.create(
                    name=getattr(language, lang + "_name"),
                    proficiency=language.proficiency,
                    row=language.row,
                    icon=language.icon,
                    language=translation_model.objects.get(language=lang),
                )
