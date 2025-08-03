from django.contrib import admin

from .models import Project, User

# pyre-ignore[16]
admin.site.register(Project)
admin.site.register(User)
