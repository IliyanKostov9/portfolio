from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.resume.data_class.portfolio import Portfolio


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
        technology_category_tr_model = apps.get_model(
            Portfolio.app_name, "TechnologyCategoryTranslation"
        )

        technology_model.objects.all().delete()

        technologies: list[Technology] = Technology.from_yaml("technology.yaml")

        for technology in technologies:
            category: Any = technology_category_tr_model.objects.get(
                name=technology.category, language_code="en"
            )

            technology_model.objects.create(
                name=technology.name,
                icon=technology.icon,
                category=category.master,
                row=technology.row,
                page=technology.page,
            )
