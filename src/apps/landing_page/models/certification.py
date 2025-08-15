from django.db.models import CharField, IntegerField, Model


class Certification(Model):
    image: CharField = CharField("Image of the certificate", max_length=30)
    row: IntegerField = IntegerField("Row number of the certificate")
    date: CharField = CharField("Date of the certificate")
    name: CharField = CharField("Name of the certificate")
    url: CharField = CharField("Url of the certificate to verify")
    # TODO: Don't manually align this card by using margin
    style: CharField = CharField("Custom css of the certificate", max_length=300)
