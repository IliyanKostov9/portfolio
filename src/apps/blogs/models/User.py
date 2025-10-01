from typing import Any

from django.db.models import CharField
from typing_extensions import override

from apps.blogs.models.Blog import Blog
from apps.blogs.models.portfolio import Portfolio


class User(Portfolio):
    # NOTE: Create TOTP
    username: CharField = CharField("Username of the user")
    password: CharField = CharField("Password of the user")

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
