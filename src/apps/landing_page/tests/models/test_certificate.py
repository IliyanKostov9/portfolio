from typing import Any

from apps.landing_page.data_class.portfolio.certification import (
    Certification as CertificatationDataClass,
)
from apps.landing_page.models.certification import Certification
from apps.landing_page.tests.models.portfolio import Portfolio


class CertificationTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        certification_model: Any = self.model.apps.get_model(
            "landing_page", "Certification"
        )

        certification_dc: list[Any] = CertificatationDataClass.from_yaml(
            "portfolio/certificate.yaml"
        )

        for certification_dc in certification_dc:
            certification: Certification = certification_model.objects.get(
                name=certification_dc.name
            )

            self.assertEqual(certification_dc.image, certification.image)
            self.assertEqual(certification_dc.date, certification.date)
            self.assertEqual(certification_dc.url, certification.url)
            self.assertEqual(certification_dc.style, certification.style)
            self.assertEqual(certification_dc.row, certification.row)

        super().tearDownClass()

    def test_clean(self):
        self.setUp()

        certifications: list[Certification] = (
            self.model.apps.get_model("landing_page", "Certification")
            .objects.all()
            .values()
        )

        certification_model = Certification()
        certification_model.clean(certifications)

        for certification in certifications:
            self.assertIsNone(certification.get("id"), True)

        super().tearDownClass()

    def test_transform(self):
        self.setUp()
        certification_model: Any = self.model.apps.get_model(
            "landing_page", "Certification"
        )

        certification = Certification()
        certificates_transformed = certification.transform()

        for certs in certificates_transformed:
            self.assertTrue(certs.get("row"))
            self.assertTrue(certs.get("certificate"))

            for cert in certs["certificate"]:
                cert_model = certification_model.objects.get(name=cert["name"])

                self.assertEqual(cert_model.image, cert["image"])
                self.assertEqual(cert_model.date, cert["date"])
                self.assertEqual(cert_model.url, cert["url"])
                self.assertEqual(cert_model.issuer, cert["issuer"])
                self.assertEqual(cert_model.style, cert["style"])

        super().tearDownClass()
