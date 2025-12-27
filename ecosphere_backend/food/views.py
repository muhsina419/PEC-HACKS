from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import EcoPlateEntry
from .serializers import EcoPlateEntrySerializer


def _packaging_factor(packaging_type: str) -> float:
    packaging_type = packaging_type.lower()
    if packaging_type == "plastic":
        return 2.5
    if packaging_type == "paper":
        return 1.0
    if packaging_type == "compostable":
        return 0.4
    if packaging_type == "reusable":
        return 0.2
    return 1.5


def _delivery_factor(delivery_mode: str) -> float:
    delivery_mode = delivery_mode.lower()
    if delivery_mode == "bike":
        return 0.05
    if delivery_mode == "ev":
        return 0.07
    if delivery_mode == "car":
        return 0.25
    return 0.12


def _meal_base(meal_type: str) -> float:
    meal_type = meal_type.lower()
    if any(tag in meal_type for tag in ["meat", "mutton", "beef", "pork"]):
        return 2.5
    if "chicken" in meal_type:
        return 1.8
    if "dairy" in meal_type:
        return 1.2
    if any(tag in meal_type for tag in ["vegetarian", "veg", "salad", "vegan"]):
        return 0.6
    return 1.0


def _impact_label(carbon_kg: float) -> str:
    if carbon_kg < 2:
        return "Low"
    if carbon_kg < 5:
        return "Medium"
    return "High"


def _suggestion(packaging_type: str) -> str:
    if packaging_type == "plastic":
        return "Switch to reusable tiffin partner restaurants to cut packaging impact."
    if packaging_type == "paper":
        return "Choose compostable or reusable containers for your next order."
    if packaging_type == "compostable":
        return "Great choice! Ask if a refillable container option is available."
    if packaging_type == "reusable":
        return "Keep using your tiffin partners and return containers after use."
    return "Check with the restaurant for low-waste or reusable packaging options."


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def eco_plate_entry(request):
    serializer = EcoPlateEntrySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    payload = serializer.validated_data
    meal_type = payload["meal_type"]
    packaging_type = payload["packaging_type"]
    delivery_mode = payload["delivery_mode"]
    distance_km = float(payload["distance_km"])

    carbon_kg = round(
        _meal_base(meal_type)
        + _packaging_factor(packaging_type)
        + distance_km * _delivery_factor(delivery_mode),
        2,
    )

    impact_label = _impact_label(carbon_kg)
    suggestion = _suggestion(packaging_type)

    entry = EcoPlateEntry.objects.create(
        user=request.user,
        meal_type=meal_type,
        packaging_type=packaging_type,
        delivery_mode=delivery_mode,
        distance_km=distance_km,
        carbon_kg=carbon_kg,
        impact_label=impact_label,
        suggestion=suggestion,
        bill_reference=payload.get("bill_reference", ""),
    )

    message = f"{packaging_type.title()} + {distance_km:g}km Delivery → {carbon_kg} kg CO₂e ({impact_label} Impact)"

    return Response(
        {
            "message": message,
            "entry": EcoPlateEntrySerializer(entry).data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_eco_plate_entries(request):
    entries = EcoPlateEntry.objects.filter(user=request.user)
    return Response(EcoPlateEntrySerializer(entries, many=True).data)
