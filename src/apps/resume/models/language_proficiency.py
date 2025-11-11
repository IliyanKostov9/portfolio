from typing import Any, Final

from django.db.models import CASCADE, CharField, ForeignKey, IntegerField
from django.forms.models import model_to_dict
from django.utils.translation import get_language
from typing_extensions import override

from apps.resume.models.portfolio import Portfolio
from apps.resume.models.translation import Translation

LANGUAGE_LEVEL_PROFICIENCY: Final[dict[str, int]] = {
    "Beginner": 25,
    "Intermidiate": 50,
    "Advanced": 75,
    "Fluent": 100,
    "Native": 100,
}

LANGUAGE_LEVEL_COLORS: Final[dict[str, str]] = {
    "Beginner": "bg-danger",
    "Intermidiate": "bg-warning",
    "Advanced": "",
    "Fluent": "bg-success",
    "Native": "bg-success",
}


class LanguageProficiency(Portfolio):
    name: CharField = CharField("Name of the language", max_length=50)
    proficiency: CharField = CharField("Proficiency of the language", max_length=50)
    icon: CharField = CharField("Flag of the language", max_length=50)
    row: IntegerField = IntegerField("Row number of the language")
    language: ForeignKey = ForeignKey(
        Translation,
        verbose_name="Translated language name",
        on_delete=CASCADE,
    )

    @override
    def get_all(self) -> Any:
        return list(LanguageProficiency.objects.filter(language=get_language()))

    @override
    def transform(self) -> Any:
        languages_objs = [model_to_dict(wh) for wh in self.get_all()]

        self.clean(languages_objs)

        rows = {}
        result = []
        for language in languages_objs:
            row = language["row"]
            if row not in rows:
                rows[row] = {"row": row, "language": []}
                result.append(rows[row])
            language.pop("row")

            language["level"] = LANGUAGE_LEVEL_PROFICIENCY.get(language["proficiency"])
            language["level_color"] = LANGUAGE_LEVEL_COLORS.get(language["proficiency"])
            rows[row]["language"].append(language)

        return result

    @override
    def clean(self, languages_objs: list[Any]) -> None:
        for language in languages_objs:
            language.pop("id")
