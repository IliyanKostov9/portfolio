from dataclasses import dataclass
from typing import Any

from landing_page.data_class.portfolio.portfolio import Portfolio
from typing_extensions import override


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
        technology_category_model.objects.all().delete()

        technology_categories: list[TechnologyCategory] = TechnologyCategory.from_yaml(
            "portfolio/technology_category.yaml"
        )

        for technology_category in technology_categories:
            technology_category_model.objects.create(name=technology_category.name)
