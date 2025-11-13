from typing import Any

from django.db.models import CharField
from typing_extensions import override

from apps.resume.models.portfolio import Portfolio


class Translation(Portfolio):
    language: CharField = CharField(
        "The language to translate to", max_length=50, primary_key=True
    )

    @override
    def get_all(self) -> Any:
        return list(Translation.objects.all().values())

    @override
    def transform(self) -> Any:
        pass

    @override
    def clean(self) -> None:
        pass
