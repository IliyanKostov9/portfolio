from django.db.models import CharField, Model


class TechnologyCategory(Model):
    name: CharField = CharField(
        "Name of the technology category", max_length=50, primary_key=True
    )
