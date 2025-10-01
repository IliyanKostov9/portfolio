from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.resume.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class Project(Portfolio):
    name: str
    description: str
    scroll_description: bool
    image: str
    date: str
    row: int
    repositories: dict[str, str]

    @classmethod
    def from_yaml(cls, path: str) -> list["Project"]:
        defaults = {
            "scroll_description": False,
        }
        objects: Any = super().read_yaml(path)

        return [cls(**{**defaults, **obj}) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        project_model = apps.get_model(Portfolio.app_name, "Project")
        project_model.objects.all().delete()

        projects: list[Project] = Project.from_yaml("project.yaml")

        for project in projects:
            project_model.objects.create(
                name=project.name,
                description=project.description,
                scroll_description=project.scroll_description,
                image=project.image,
                date=project.date,
                row=project.row,
                repositories=project.repositories,
            )
