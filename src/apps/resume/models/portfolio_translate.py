from typing import Any

from parler.models import TranslatableModel


class PortfolioTranslate(TranslatableModel):
    """
    Interface for all of the translatable models to inherit and override methods
    """

    def get_all(self) -> Any:
        pass

    def transform(self) -> Any:
        pass

    def clean(self) -> None:
        pass

    class Meta:
        abstract: bool = True
        app_label: str = "resume"
