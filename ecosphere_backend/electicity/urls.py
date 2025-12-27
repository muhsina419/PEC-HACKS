from django.urls import path
from .views import upload_electricity_bill

urlpatterns = [
    path("upload/", upload_electricity_bill),
]
