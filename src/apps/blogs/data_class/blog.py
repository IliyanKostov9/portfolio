from dataclasses import dataclass
from datetime import date
from typing import Any

from typing_extensions import override

from apps.blogs.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class Blog(Portfolio):
    title: str
    description: str
    image_preview: str
    date: date
    url: str
    read_time_mins: int
    category: int
    row: int

    @classmethod
    def from_yaml(cls, path: str) -> list["Blog"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps) -> None:
        blog_model = apps.get_model(Portfolio.app_name, "Blog")
        blog_category_model = apps.get_model(Portfolio.app_name, "BlogCategory")

        blog_model.objects.all().delete()

        blogs: list[Blog] = Blog.from_yaml("blog.yaml")

        for blog in blogs:
            blog_model.objects.create(
                title=blog.title,
                description=blog.description,
                image_preview=blog.image_preview,
                date=blog.date,
                url=blog.url,
                read_time_mins=blog.read_time_mins,
                row=blog.row,
                category=blog_category_model.objects.get(name=blog.category),
            )
