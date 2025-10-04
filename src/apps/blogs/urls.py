from django.urls import path

from apps.blogs.views.home.blogs_view import BlogsView
from apps.blogs.views.monitor.csp_report_view import CSPReportView

urlpatterns = [
    path("blogs", BlogsView.as_view(), name="blogs"),
    path("monitor/csp-report", CSPReportView.as_view(), name="csp-report"),
]
