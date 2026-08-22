from typing import Any, override

from django.db.models import CharField, ImageField, IntegerField
from django.forms.models import model_to_dict

from apps.resume.models.portfolio import Portfolio


class Certification(Portfolio):
    image: ImageField = ImageField(
        "Image of the certificate",
        blank=False,
        null=False,
    )
    row: IntegerField = IntegerField("Row number of the certificate")
    date: CharField = CharField("Date of the certificate")
    name: CharField = CharField("Name of the certificate")
    url: CharField = CharField("Url of the certificate to verify")
    issuer: CharField = CharField("Issuer of the certificate")

    @override
    def get_all(self) -> Any:
        return list(Certification.objects.all())

    @override
    def transform(self) -> Any:
        certifications_objs = [
            model_to_dict(certification) for certification in self.get_all()
        ]

        self.clean(certifications_objs)

        rows = {}
        result = []
        for cert in certifications_objs:
            row = cert["row"]
            if row not in rows:
                rows[row] = {"row": row, "certificate": []}
                result.append(rows[row])
            cert.pop("row")
            rows[row]["certificate"].append(cert)

        return result

    @override
    def clean(self, certifications_obj: list[Any]) -> None:
        for certificate in certifications_obj:
            certificate.pop("id")
