from typing import Any


class Portfolio:
    """
    Interface for all of the models to inhecit and override methods
    """

    def get_all(self) -> Any:
        pass

    def transform(self) -> Any:
        pass

    def clean(self) -> None:
        pass
