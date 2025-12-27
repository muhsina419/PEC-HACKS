from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import HomeApplianceUsage, HomeEnergyAssessment
from .serializers import (
    ApplianceInputSerializer,
    EMISSION_FACTOR,
    ElectricityBillSerializer,
    HomeEnergyAssessmentSerializer,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_electricity_bill(request):
    serializer = ElectricityBillSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        bill = serializer.save()
        return Response(ElectricityBillSerializer(bill).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def _efficiency_factor(star_rating: int) -> float:
    return max(0.5, 1.2 - (star_rating * 0.1))


def _appliance_suggestion(name: str, star_rating: int, wattage: float) -> str:
    lowered = name.lower()
    if "ac" in lowered or "air" in lowered:
        return "Consider inverter/5-star AC or pairing with solar to cut cooling load."
    if "light" in lowered or "bulb" in lowered:
        return "Swap to LED lighting and timers for reduced energy use."
    if star_rating <= 3:
        return "Upgrade to a higher star-rated appliance for better efficiency."
    if wattage > 1200:
        return "Shift heavy loads to off-peak hours or offset with rooftop solar."
    return "Use smart plugs or schedules to curb standby and idle consumption."


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_home_energy_assessment(request):
    serializer = ApplianceInputSerializer(data=request.data.get("appliances", []), many=True)
    if not serializer.is_valid():
        return Response({"appliances": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    if not serializer.validated_data:
        return Response({"appliances": "At least one appliance is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill_id = request.data.get("bill_id")
    bill = None
    if bill_id:
        from .models import ElectricityBill

        bill = ElectricityBill.objects.filter(id=bill_id, user=request.user).first()
        if bill is None:
            return Response({"bill_id": "No matching electricity bill found"}, status=status.HTTP_400_BAD_REQUEST)

    validated = serializer.validated_data
    appliances = []
    total_carbon = 0

    for entry in validated:
        wattage = float(entry["wattage"])
        hours = float(entry["hours_per_day"])
        star_rating = int(entry["star_rating"])

        monthly_kwh = (wattage * hours * 30) / 1000
        carbon_kg = round(monthly_kwh * EMISSION_FACTOR * _efficiency_factor(star_rating), 2)
        total_carbon += carbon_kg

        appliances.append(
            HomeApplianceUsage(
                appliance_name=entry["name"],
                wattage=wattage,
                star_rating=star_rating,
                hours_per_day=hours,
                carbon_kg=carbon_kg,
                suggestion=_appliance_suggestion(entry["name"], star_rating, wattage),
            )
        )

    assessment = HomeEnergyAssessment.objects.create(
        user=request.user, bill=bill, total_carbon_kg=round(total_carbon, 2)
    )

    for appliance in appliances:
        appliance.assessment = assessment
        appliance.save()

    top_appliance = max(appliances, key=lambda a: a.carbon_kg) if appliances else None
    headline = ""
    if top_appliance and total_carbon:
        share = (top_appliance.carbon_kg / total_carbon) * 100
        headline = f"{top_appliance.appliance_name} = {share:.0f}% of home energy carbon"

    return Response(
        {
            "headline": headline,
            "total_carbon_kg": assessment.total_carbon_kg,
            "assessment": HomeEnergyAssessmentSerializer(assessment).data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_home_energy_assessments(request):
    assessments = HomeEnergyAssessment.objects.filter(user=request.user).order_by("-created_at")
    data = [HomeEnergyAssessmentSerializer(assessment).data for assessment in assessments]
    return Response(data)
