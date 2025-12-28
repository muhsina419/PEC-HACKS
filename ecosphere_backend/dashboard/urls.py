from django.urls import path

from .views import CarbonFootprintView

urlpatterns = [
    path("carbon/", CarbonFootprintView.as_view(), name="carbon-footprint"),
]
