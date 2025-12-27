from django.urls import path

from .views import eco_food_scan, list_inventory, log_user_action, scan_and_store

urlpatterns = [
    path("scan/", scan_and_store),
    path("list/", list_inventory),
    path("actions/", log_user_action),
    path("food/", eco_food_scan),
]
