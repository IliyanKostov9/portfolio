from typing import Any

from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    ManyToManyField,
    OneToOneField,
)
from typing_extensions import override

from apps.blogs.models.Blog import Blog
from apps.blogs.models.User import User
from apps.blogs.models.portfolio import Portfolio


class Comment(Portfolio):
    message: CharField = CharField("Message on the comment")
    reply: ManyToManyField = ManyToManyField("self", blank=True, symmetrical=True)
    blogs: ForeignKey = ForeignKey(
        Blog,
        verbose_name="Blogs for which the comments are commented about",
        on_delete=CASCADE,
    )
    user: OneToOneField = OneToOneField(
        User,
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
