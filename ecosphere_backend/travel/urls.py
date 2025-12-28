from django.urls import path

from .views import create_commute_log, list_commute_logs, travel_summary

urlpatterns = [
    path("commutes/", create_commute_log),
    path("commutes/history/", list_commute_logs),
    path("summary/", travel_summary),
]
