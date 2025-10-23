from typing import Any

from django.db import models


class Portfolio(models.Model):
    """
    Interface for all of the models to inherit and override methods
    """

    def get_all(self) -> Any:
        """Override"""

    def transform(self) -> Any:
        """Override"""

    def clean(self) -> None:
        """Override"""

    class Meta:
        abstract: bool = True
        app_label: str = "blogs"
