from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ElectricityBill

EMISSION_FACTOR = 0.82  # kg CO2 per unit

@api_view(["POST"])
def upload_electricity_bill(request):
    current = float(request.data.get("current"))
    previous = float(request.data.get("previous"))

    units = current - previous
    carbon = units * EMISSION_FACTOR

    ElectricityBill.objects.create(
        user=request.user,
        meter_reading_current=current,
        meter_reading_previous=previous,
        units=units,
        carbon_kg=carbon
    )

    return Response({
        "units": units,
        "carbon_kg": carbon,
        "status": "Saved successfully"
    })
