import datetime
from dataclasses import dataclass
from typing import Any, override

from apps.common.data_class.translation import Translation
from portfolio.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class Blog(Portfolio):
    en_title: str
    bg_title: str
    fr_title: str
    ge_title: str

    en_description: str
    bg_description: str
    fr_description: str
    ge_description: str

    image_preview: str
    date: datetime.date
    url: str
    read_time_mins: int
    category: int
    row: int

    @classmethod
    def from_yaml(cls, path: str) -> list[Blog]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps) -> None:
        blog_model = apps.get_model("blogs", "Blog")
        blog_category_model = apps.get_model("blogs", "BlogCategory")
        translation_model = apps.get_model("common", "Translation")

        blog_model.objects.all().delete()

        for blog in Blog.from_yaml("blog.yaml"):
            for lang in Translation.languages:
                blog_model.objects.create(
                    title=getattr(blog, lang + "_title"),
                    description=getattr(blog, lang + "_description"),
                    image_preview="images/blogs/" + blog.image_preview,
                    date=blog.date,
                    url=blog.url,
                    read_time_mins=blog.read_time_mins,
                    row=blog.row,
                    category=blog_category_model.objects.get(name=blog.category),
                    language=translation_model.objects.get(language=lang),
                )
