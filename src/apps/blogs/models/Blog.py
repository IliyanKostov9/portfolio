from typing import Any

from django.db.models import CASCADE, CharField, DateField, ForeignKey, IntegerField
from typing_extensions import override

from apps.blogs.models.BlogCategory import BlogCategory
from apps.blogs.models.portfolio import Portfolio


class Blog(Portfolio):
    title: CharField = CharField("Title of the blog", max_length=100)
    description: CharField = CharField("Description of the blog", max_length=100)
    image_preview: CharField = CharField("Image preview of the blog", max_length=30)
    date: DateField = DateField("Date of the blog being posted", max_length=30)
    page_name: CharField = CharField(
        "Name of the page of the blog, where the user can navigate to"
    )
    read_time_mins: IntegerField = IntegerField(
        "Number of minutes for the reader to read the blog"
    )
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
