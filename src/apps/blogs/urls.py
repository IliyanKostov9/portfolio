from django.urls import path

from apps.blogs.views.home.home_view import HomeView
from apps.blogs.views.monitor.csp_report_view import CSPReportView

urlpatterns = [
    path("blogs", HomeView.as_view(), name="blogs"),
    path("monitor/csp-report", CSPReportView.as_view(), name="csp-report"),
]
