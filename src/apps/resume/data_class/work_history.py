from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.resume.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class WorkHistory(Portfolio):
    company_name: str
    company_name_label: str
    image: str
    en_specialty: int
    bg_specialty: int
    fr_specialty: int
    ge_specialty: int
    dates: list[str]

    en_description: str
    bg_description: str
    fr_description: str
    ge_description: str

    @classmethod
    def from_yaml(cls, path: str) -> list["WorkHistory"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        work_history_model = apps.get_model(Portfolio.app_name, "WorkHistory")
        translation_model = apps.get_model(Portfolio.app_name, "Translation")

        work_history_model.objects.all().delete()

        for work_history in WorkHistory.from_yaml("work_history.yaml"):
            for lang in Portfolio.languages:
                work_history_model.objects.create(
                    company_name=work_history.company_name,
                    company_name_label=work_history.company_name_label,
                    image=work_history.image,
                    specialty=getattr(work_history, lang + "_specialty"),
                    dates=work_history.dates,
                    description=getattr(work_history, lang + "_description"),
                    language=translation_model.objects.get(language=lang),
                )
