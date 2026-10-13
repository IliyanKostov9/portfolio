from django.urls import path

from apps.blogs.views.blogs.blogs_view import BlogsView
from apps.blogs.views.blogs.living_abroad import LivingAbroadView
from apps.blogs.views.home.voice_view import VoiceView

app_name = "blogs"

urlpatterns = [
    path("", BlogsView.as_view(), name="blogs"),
    path(
        "living-abroad",
        LivingAbroadView.as_view(),
        name="living_abroad",
    ),
    path(
        "home/voice/",
        VoiceView.as_view(),
        name="home/voice",
    ),
]
