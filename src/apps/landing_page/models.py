from django.db import models


class Project(models.Model):
    name = models.CharField("project name",max_length=200)
    link = models.CharField("Link to project",max_length=100)
    description = models.CharField("Short description of the project",max_length=2000)


class User(models.Model):
    name = models.CharField("Name of the user",max_length=200)
    email = models.EmailField("Email of the user",max_length=200)
    avatar = models.ImageField(name=f"{name}-avatar", width_field=300, height_field=300)
    skills = models.CharField("Skillsets",max_length=200)
    projects = models.ForeignKey(
        Project, on_delete=models.RESTRICT
    )  # TODO: Check what restrict does
