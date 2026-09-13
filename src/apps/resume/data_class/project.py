from dataclasses import dataclass
from typing import Any, override

from apps.common.data_class.translation import Translation
from portfolio.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class Project(Portfolio):
    en_name: str
    bg_name: str
    fr_name: str
    ge_name: str

    en_description: str
    bg_description: str
    fr_description: str
    ge_description: str

    scroll_description: bool
    image: str
    date: str
    row: int
    repositories: dict[str, str]

    @classmethod
    def from_yaml(cls, path: str) -> list[Project]:
        defaults = {
            "scroll_description": False,
        }
        objects: Any = super().read_yaml(path)

        return [cls(**{**defaults, **obj}) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        project_model = apps.get_model("resume", "Project")
        translation_model = apps.get_model("common", "Translation")

        project_model.objects.all().delete()

        for project in Project.from_yaml("project.yaml"):
            for lang in Translation.languages:
                project_model.objects.create(
                    name=getattr(project, lang + "_name"),
                    description=getattr(project, lang + "_description"),
                    scroll_description=project.scroll_description,
                    image="images/" + project.image,
                    date=project.date,
                    row=project.row,
                    repositories=project.repositories,
                    language=translation_model.objects.get(language=lang),
                )
