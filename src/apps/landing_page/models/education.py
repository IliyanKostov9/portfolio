from django.db.models import BooleanField, CharField, Model


class Education(Model):
    degree: CharField = CharField("Degree name", max_length=100)
    specialty: CharField = CharField("Specialty name", max_length=100)
    university_name: CharField = CharField("University name", max_length=50)
    description: CharField = CharField("Description of the education", max_length=300)
    scroll_description: BooleanField = BooleanField(
        "Whether or not the description should be scrollable or not"
    )
    image: CharField = CharField("Image of the education", max_length=30)
    href_tooltip: CharField = CharField("Href tooltip of the education", max_length=30)
    href_title: CharField = CharField("Href title of the education", max_length=200)
    date: CharField = CharField("Date of the education")
    gpa: CharField = CharField("GPA of the education")
