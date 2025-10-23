import os
from abc import ABC, abstractmethod
from typing import Any, Final

import yaml


class Portfolio(ABC):
    app_name: Final[str] = "blogs"

    @classmethod
    def read_yaml(cls, path: str) -> Any:
        parent_dir: str = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "config")
        )

        if not path.endswith((".yaml", ".yml")):
            raise InterruptedError("File must end with yml or yaml!")

        with open(os.path.join(parent_dir, path), "r") as file:
            return yaml.safe_load(file)

    @abstractmethod
    def table_create(self):
        pass
