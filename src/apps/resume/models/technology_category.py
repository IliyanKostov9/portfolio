from typing import Any

from django.db.models import PROTECT, CharField, ForeignKey
from typing_extensions import override

from apps.resume.models.portfolio import Portfolio
from apps.resume.models.translation import Translation


class TechnologyCategory(Portfolio):
    name: CharField = CharField(
        "Name of the technology category", max_length=50, primary_key=True
    )
    language: ForeignKey = ForeignKey(
        Translation,
        verbose_name="Translated category name of the technology",
        on_delete=PROTECT,
        null=True,
    )

    mapped_to: CharField = CharField(
        "The english equivalent version to map the translated name to",
    )

    @override
    def get_all(self) -> Any:
        return list(TechnologyCategory.objects.all().values())

    @override
    def transform(self) -> Any:
        pass

    @override
    def clean(self) -> None:
        pass
