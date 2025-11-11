from dataclasses import dataclass
from typing import Any

from django.utils import translation
from typing_extensions import override

from apps.resume.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class TechnologyCategory(Portfolio):
    name: str

    @classmethod
    def from_yaml(cls, path: str) -> list["TechnologyCategory"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        technology_category_model = apps.get_model(
            Portfolio.app_name, "TechnologyCategory"
        )
        technology_category_tr_model = apps.get_model(
            Portfolio.app_name, "TechnologyCategoryTranslation"
        )

        technology_category_model.objects.all().delete()
        technology_category_tr_model.objects.all().delete()

        for lang in Portfolio.languages:
            translation.activate(lang)
            for technology_category in TechnologyCategory.from_yaml(
                f"{lang}/technology_category.yaml"
            ):
                cat = technology_category_model.objects.create()  # create base
                cat.set_current_language(lang)  # select translation
                cat.save()
