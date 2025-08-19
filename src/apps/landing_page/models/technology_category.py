from typing import Any

from django.db.models import CharField
from landing_page.models.portfolio import Portfolio
from typing_extensions import override


class TechnologyCategory(Portfolio):
    name: CharField = CharField(
        "Name of the technology category", max_length=50, primary_key=True
    )

    @override
    def get_all(self) -> Any:
        pass

    @override
    def transform(self) -> Any:
        pass

    @override
    def clean(self) -> None:
        pass
