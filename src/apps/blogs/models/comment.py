from typing import Any

from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    ManyToManyField,
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
    user: ForeignKey = ForeignKey(
        User,
        on_delete=CASCADE,
    )

    @override
    def get_all(self) -> Any:
        return list(Comment.objects.all().values())

    @override
    def transform(self) -> Any:
        comment_objs = self.get_all()

        self.clean(comment_objs)

        rows = {}
        result = []
        for comment in comment_objs:
            row = comment["row"]
            if row not in rows:
                rows[row] = {"row": row, "comment": []}
                result.append(rows[row])
            comment.pop("row")
            rows[row]["blog"].append(comment)

        return result

    @override
    def clean(self, comment_obj: list[Any]) -> None:
        for comment in comment_obj:
            comment.pop("id")
