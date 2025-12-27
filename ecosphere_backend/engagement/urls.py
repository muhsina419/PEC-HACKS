from django.urls import path

from . import views

urlpatterns = [
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("groups/", views.groups, name="groups"),
    path("groups/join/", views.join_group, name="join_group"),
    path("events/", views.events, name="events"),
    path("events/rsvp/", views.rsvp_event, name="rsvp_event"),
    path("reports/", views.list_reports, name="list_reports"),
    path("reports/create/", views.create_report, name="create_report"),
    path("reports/<int:pk>/verify/", views.verify_report, name="verify_report"),
    path("badges/", views.badges, name="badges"),
    path("reminders/", views.reminders, name="reminders"),
    path("reminders/create/", views.create_reminder, name="create_reminder"),
    path("eco-shop/", views.eco_shop, name="eco_shop"),
]
