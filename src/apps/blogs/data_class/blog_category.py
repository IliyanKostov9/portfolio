from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.blogs.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class BlogCategory(Portfolio):
    name: str

    @classmethod
    def from_yaml(cls, path: str) -> list["BlogCategory"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        blog_category_model = apps.get_model(Portfolio.app_name, "BlogCategory")
        blog_category_model.objects.all().delete()

        blog_categories: list[BlogCategory] = BlogCategory.from_yaml(
            "blog_category.yaml"
        )

        for blog_category in blog_categories:
            blog_category_model.objects.create(
                name=blog_category.name,
            )
