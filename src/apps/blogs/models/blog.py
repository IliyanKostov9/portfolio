from typing import Any, override

from django.db.models import (
    CASCADE,
    CharField,
    DateField,
    ForeignKey,
    ImageField,
    IntegerField,
)

from apps.blogs.models.blog_category import BlogCategory
from apps.blogs.models.portfolio import Portfolio


class Blog(Portfolio):
    title: CharField = CharField("Title of the blog", max_length=100)
    description: CharField = CharField("Short description of the blog")
    image_preview: ImageField = ImageField(
        "Image preview of the blog", blank=False, null=False
    )
    date: DateField = DateField("Date of the blog being posted", max_length=30)
    url: CharField = CharField(
        "Name of the page of the blog, where the user can navigate to"
    )
    read_time_mins: IntegerField = IntegerField(
        "Number of minutes for the reader to read the blog"
    )
    row: IntegerField = IntegerField("Row number of the blog")
    category: ForeignKey = ForeignKey(
        BlogCategory,
        verbose_name="Category of which blog it belongs to (life, technology, project, etc)",
        on_delete=CASCADE,
    )

    @override
    def get_all(self) -> Any:
        return list(Blog.objects.all().values())

    @override
    def transform(self) -> Any:
        blog_objs = self.get_all()

        self.clean(blog_objs)

        rows = {}
        result = []
        for blog in blog_objs:
            row = blog["row"]
            if row not in rows:
                rows[row] = {"row": row, "blog": []}
                result.append(rows[row])
            blog.pop("row")
            rows[row]["blog"].append(blog)

        return result

    @override
    def clean(self, blog_obj: list[Any]) -> None:
        for blog in blog_obj:
            blog.pop("id")
