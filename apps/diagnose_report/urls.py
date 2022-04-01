from django.urls import path
from . import handlers


urlpatterns = [
    path("report-intializer", handlers.report_handler),
    path("report-stage-checker", handlers.diagnose_report_stage_checker),
]
