from typing import Any

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    IntegerField,
    JSONField,
)
from django.forms.models import model_to_dict
from django.utils.translation import get_language
from typing_extensions import override

from apps.resume.models.portfolio import Portfolio
from apps.resume.models.translation import Translation


class Project(Portfolio):
    name: CharField = CharField("Name of the project", max_length=50)
    description: CharField = CharField("Description of the project", max_length=300)
    scroll_description: BooleanField = BooleanField(
        "Whether or not the description should be scrollable or not",
        null=True,
    )
    image: CharField = CharField("Image of the project", max_length=30)
    date: CharField = CharField("Date of the project being worked on")
    row: IntegerField = IntegerField("Row number of the project")
    repositories: JSONField = JSONField("Repositories")
    language: ForeignKey = ForeignKey(
        Translation,
        verbose_name="Translated version of project info",
        on_delete=CASCADE,
    )

    @override
    def get_all(self) -> Any:
        return list(Project.objects.filter(language=get_language()))

    @override
    def transform(self) -> Any:
        projects_objs = [model_to_dict(wh) for wh in self.get_all()]

        rows = {}
        result = []
        for project in projects_objs:
            row = project["row"]
            if row not in rows:
                rows[row] = {"row": row, "project": []}
                result.append(rows[row])
            project.pop("row")
            rows[row]["project"].append(project)

        return result

    @override
    def clean(self, projects_obj: list[Any]) -> None:
        for project in projects_obj:
            project.pop("id")
