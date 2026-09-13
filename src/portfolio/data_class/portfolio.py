import inspect
import os
from abc import ABC, abstractmethod
from typing import Any

import yaml


class Portfolio(ABC):
    @classmethod
    def read_yaml(cls, file_name: str) -> Any:
        parent_dir: str = os.path.abspath(
            os.path.join(os.path.dirname(inspect.getfile(cls)), "..", "config")
        )

        if not file_name.endswith((".yaml", ".yml")):
            raise InterruptedError("File must end with yml or yaml!")

        with open(os.path.join(parent_dir, file_name), "r") as file:
            return yaml.safe_load(file)

    @abstractmethod
    def table_create(self):
        pass
