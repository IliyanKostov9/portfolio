from dataclasses import dataclass
from typing import Any

from typing_extensions import override

from apps.landing_page.data_class.portfolio.portfolio import Portfolio


@dataclass(frozen=True)
class Certification(Portfolio):
    name: str
    image: str
    date: str
    url: str
    row: int
    style: str

    @classmethod
    def from_yaml(cls, path: str) -> list["Certification"]:
        objects: Any = super().read_yaml(path)

        return [cls(**obj) for obj in objects]

    @override
    @staticmethod
    def table_create(apps):
        certification_model = apps.get_model(Portfolio.app_name, "Certification")
        certification_model.objects.all().delete()

        certifications: list[Certification] = Certification.from_yaml(
            "portfolio/certificate.yaml"
        )

        for certification in certifications:
            certification_model.objects.create(
                name=certification.name,
                image=certification.image,
                url=certification.url,
                date=certification.date,
                row=certification.row,
                style=certification.style,
            )
