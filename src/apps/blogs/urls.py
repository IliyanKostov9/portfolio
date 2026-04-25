from django.urls import path

from apps.blogs.views.blogs.blogs_view import BlogsView
from apps.blogs.views.blogs.living_abroad import (
    LivingAbroadView,
)
from apps.blogs.views.monitor.csp_report_view import CSPReportView

urlpatterns = [
    path("", BlogsView.as_view(), name="blogs"),
    path(
        "living-abroad",
        LivingAbroadView.as_view(),
        name="living_abroad",
    ),
    path("monitor/csp-report", CSPReportView.as_view(), name="csp-report"),
]
