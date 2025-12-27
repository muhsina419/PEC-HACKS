from django.urls import path

from . import views

urlpatterns = [
    path("eco-plate/", views.eco_plate_entry, name="eco_plate_entry"),
    path("eco-plate/history/", views.list_eco_plate_entries, name="eco_plate_history"),
]
