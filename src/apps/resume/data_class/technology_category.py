from dataclasses import dataclass
from typing import Any, override

from apps.common.data_class.translation import Translation
from portfolio.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class TechnologyCategory(Portfolio):
    en_name: str
    bg_name: str
    fr_name: str
    ge_name: str

    @classmethod
    def from_yaml(cls, path: str) -> list[TechnologyCategory]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        technology_category_model = apps.get_model("resume", "TechnologyCategory")
        translation_model = apps.get_model("common", "Translation")

        technology_category_model.objects.all().delete()

        for technology_category in TechnologyCategory.from_yaml(
            "technology_category.yaml"
        ):
            for lang in Translation.languages:
                technology_category_model.objects.create(
                    name=getattr(technology_category, lang + "_name"),
                    language=translation_model.objects.get(language=lang),
                    mapped_to=technology_category.en_name,
                )
