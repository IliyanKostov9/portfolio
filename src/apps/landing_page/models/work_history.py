from typing import Any

import markdown
from django.db.models import CharField, JSONField, Model
from landing_page.models.portfolio import Portfolio
from typing_extensions import override


class WorkHistory(Model, Portfolio):
    company_name: CharField = CharField("Company name", max_length=100)
    company_name_label: CharField = CharField(
        "Aria label of the company in pattern company-name-123", max_length=100
    )
    image: CharField = CharField("Image of the company", max_length=30)
    specialty: CharField = CharField("Specialty name", max_length=100)
    dates: JSONField = JSONField("Dates of work")
    description: CharField = CharField("Description of the work history")

    @override
    def get_all(self) -> Any:
        return list(WorkHistory.objects.all().values())

    @override
    def transform(self) -> Any:
        work_history_objs = self.get_all()
        self.clean(work_history_objs)

        return work_history_objs

    @override
    def clean(self, work_histories: list[Any]) -> None:
        for work_history in work_histories:
            work_history.pop("id")

    def set_description_markdown(self, work_histories: list[Any]) -> None:
        """
        Not used currently
        """
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        for work_history in work_histories:
            work_history["description"] = md.convert(work_history["description"])
