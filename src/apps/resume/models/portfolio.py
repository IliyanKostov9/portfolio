from typing import Any

from django.db import models


class Portfolio(models.Model):
    """
    Interface for all of the models to inherit and override methods
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
