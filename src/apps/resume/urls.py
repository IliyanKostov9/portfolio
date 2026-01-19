from django.urls import path

from apps.resume.views.home.contact_me_view import ContactMeView
from apps.resume.views.home.home_view import HomeView
from apps.resume.views.monitor.csp_report_view import CSPReportView
from apps.resume.views.home.cv_download_view import CVDownloadView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("home/contact-me/", ContactMeView.as_view(), name="home/contact-me"),
    path("home/cv-download/", CVDownloadView.as_view(), name="home/cv-download"),
    path("monitor/csp-report", CSPReportView.as_view(), name="csp-report"),
]
