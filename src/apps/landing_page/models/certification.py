from typing import Any

from django.db.models import CharField, IntegerField
from typing_extensions import override

from apps.landing_page.models.portfolio import Portfolio


class Certification(Portfolio):
    image: CharField = CharField("Image of the certificate", max_length=30)
    row: IntegerField = IntegerField("Row number of the certificate")
    date: CharField = CharField("Date of the certificate")
    name: CharField = CharField("Name of the certificate")
    url: CharField = CharField("Url of the certificate to verify")
    # TODO: Don't manually align this card by using margin
    style: CharField = CharField("Custom css of the certificate", max_length=300)

    @override
    def get_all(self) -> Any:
        return list(Certification.objects.all().values())

    @override
    def transform(self) -> Any:
        certifications_objs = self.get_all()

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
