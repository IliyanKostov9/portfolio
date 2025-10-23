from django.urls import path

from apps.blogs.views.blogs.blogs_view import BlogsView
from apps.blogs.views.blogs.the_start_of_something_new_view import (
    TheStartOfSomethingNewView,
)
from apps.blogs.views.monitor.csp_report_view import CSPReportView

urlpatterns = [
    path("blogs/", BlogsView.as_view(), name="blogs"),
    path(
        "blogs/the-start-of-something-new",
        TheStartOfSomethingNewView.as_view(),
        name="the_start_of_something_new",
    ),
    path("monitor/csp-report", CSPReportView.as_view(), name="csp-report"),
]
