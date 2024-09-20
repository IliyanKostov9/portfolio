from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    avatar = models.ImageField(name=f"{name}-avatar", width_field=300, height_field=300)
    skills = models.CharField(max_length=200)
    projects = models.ForeignKey(
        Project, on_delete=models.RESTRICT
    )  # TODO: Check what restrict does
