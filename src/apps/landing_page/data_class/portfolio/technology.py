from dataclasses import dataclass
from typing import Any

from landing_page.data_class.portfolio.portfolio import Portfolio
from typing_extensions import override


@dataclass(frozen=True)
class Technology(Portfolio):
    name: str
    icon: str
    category: int
    page: int
    row: int

    @classmethod
    def from_yaml(cls, path: str) -> list["Technology"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        technology_model = apps.get_model(Portfolio.app_name, "Technology")
        technology_category_model = apps.get_model(
            Portfolio.app_name, "TechnologyCategory"
        )

        technology_model.objects.all().delete()

        technologies: list[Technology] = Technology.from_yaml(
            "portfolio/technology.yaml"
        )

        for technology in technologies:
            category: Any = technology_category_model.objects.get(
                name=technology.category
            )

            technology_model.objects.create(
                name=technology.name,
                icon=technology.icon,
                category=category,
                row=technology.row,
                page=technology.page,
            )
