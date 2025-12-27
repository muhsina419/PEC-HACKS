from django.urls import path
from .views import (
    create_home_energy_assessment,
    list_home_energy_assessments,
    upload_electricity_bill,
)

urlpatterns = [
    path("upload/", upload_electricity_bill),
    path("home-energy/", create_home_energy_assessment),
    path("home-energy/history/", list_home_energy_assessments),
]
