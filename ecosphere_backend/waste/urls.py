from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_items),
    path("create/", views.create_item),
    path("alerts/", views.alerts),
    path("<int:pk>/disposal/", views.update_disposal),
]
