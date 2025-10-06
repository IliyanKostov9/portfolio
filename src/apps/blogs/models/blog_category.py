from typing import Any

from django.db.models import CharField
from typing_extensions import override

from apps.blogs.models.portfolio import Portfolio


class BlogCategory(Portfolio):
    name: CharField = CharField("Name of the category")

    @override
    def get_all(self) -> Any:
        return list(BlogCategory.objects.all().values())

    @override
    def transform(self) -> Any:
        blog_category_objs = self.get_all()

        self.clean(blog_category_objs)

        rows = {}
        result = []
        for blog in blog_category_objs:
            row = blog["row"]
            if row not in rows:
                rows[row] = {"row": row, "blog_category": []}
                result.append(rows[row])
            blog.pop("row")
            rows[row]["blog_category"].append(blog)

        return result

    @override
    def clean(self, blog_obj: list[Any]) -> None:
        for blog in blog_obj:
            blog.pop("id")
