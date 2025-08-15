from django.db.models import CharField, JSONField, Model


class WorkHistory(Model):
    company_name: CharField = CharField("Company name", max_length=100)
    company_name_label: CharField = CharField(
        "Aria label of the company in pattern company-name-123", max_length=100
    )
    image: CharField = CharField("Image of the company", max_length=30)
    specialty: CharField = CharField("Specialty name", max_length=100)
    dates: JSONField = JSONField("Dates of work")
    description: CharField = CharField("Description of the work history")
