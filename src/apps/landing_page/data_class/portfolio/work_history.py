from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.landing_page.data_class.portfolio.portfolio import Portfolio


@dataclass(frozen=True)
class WorkHistory(Portfolio):
    company_name: str
    company_name_label: str
    image: str
    specialty: int
    dates: list[str]
    description: list[str]

    @classmethod
    def from_yaml(cls, path: str) -> list["WorkHistory"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        work_history_model = apps.get_model(Portfolio.app_name, "WorkHistory")
        work_history_model.objects.all().delete()

        work_histories: list[WorkHistory] = WorkHistory.from_yaml(
            "portfolio/work_history.yaml"
        )

        for work_history in work_histories:
            work_history_model.objects.create(
                company_name=work_history.company_name,
                company_name_label=work_history.company_name_label,
                image=work_history.image,
                specialty=work_history.specialty,
                dates=work_history.dates,
                description=work_history.description,
            )
