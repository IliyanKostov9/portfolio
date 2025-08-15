from django.db.models import BooleanField, CharField, IntegerField, JSONField, Model


class Project(Model):
    name: CharField = CharField("Name of the project", max_length=50)
    description: CharField = CharField("Description of the project", max_length=300)
    schroll_description: BooleanField = BooleanField(
        "Whether or not the description should be scrollable or not"
    )
    image: CharField = CharField("Image of the project", max_length=30)
    date: CharField = CharField("Date of the project being worked on")
    row: IntegerField = IntegerField("Row number of the project")
    urls: JSONField = JSONField("Urls of the project")
    project_names: CharField = CharField("Project names")
