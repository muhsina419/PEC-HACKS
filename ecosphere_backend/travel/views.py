from datetime import date, timedelta

from django.db import models
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CommuteLog
from .serializers import CommuteLogSerializer


EMISSION_FACTORS = {
    "bike": 0.01,  # assumes embodied carbon only
    "bus_metro": 0.08,
    "petrol": 0.21,
    "ev": 0.08,
}


SMART_ROUTES = {
    "bike": "Smart route: safer cycle lanes + no-idle shortcuts",
    "bus_metro": "Smart route: metro + last-mile walk to avoid congestion",
    "petrol": "Smart route: mixed bus + car-pool to trim petrol miles",
    "ev": "Smart route: EV + transit park-and-ride to cut peak traffic",
}


def _weekly_change(user):
    today = date.today()
    current_start = today - timedelta(days=7)
    previous_start = current_start - timedelta(days=7)

    current_total = (
        CommuteLog.objects.filter(user=user, created_at__date__gte=current_start)
        .aggregate(total=models.Sum("carbon_kg"))
        .get("total")
        or 0
    )
    previous_total = (
        CommuteLog.objects.filter(
            user=user, created_at__date__gte=previous_start, created_at__date__lt=current_start
        )
        .aggregate(total=models.Sum("carbon_kg"))
        .get("total")
        or 0
    )

    if previous_total:
        change = round(((previous_total - current_total) / previous_total) * 100, 1)
        trend = "decreased" if change >= 0 else "increased"
        return f"Your travel footprint {trend} by {abs(change)}% this week", change

    return "Start logging commutes to see your weekly trend", None


def _eco_scan_hint(mode: str, eco_scan_bonus: bool) -> str:
    if eco_scan_bonus and mode in {"bike", "ev"}:
        return "EV/cycle scans applied — scoring bonus for low-carbon travel."
    if mode in {"bike", "ev"}:
        return "Scan your cycle/EV receipts to boost your EcoScore linkage."
    return "Scan transit passes or EV gear to connect EcoScan with commutes."


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_commute_log(request):
    serializer = CommuteLogSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    payload = serializer.validated_data
    mode = payload["mode"]
    distance_km = float(payload["distance_km"])
    eco_scan_bonus = bool(payload.get("eco_scan_bonus"))

    factor = EMISSION_FACTORS.get(mode, 0.15)
    carbon = distance_km * factor

    if eco_scan_bonus and mode in {"bike", "ev"}:
        carbon *= 0.9  # reward for linking EcoScan with low-carbon transport

    carbon = round(carbon, 2)
    route_label = payload.get("route_label") or SMART_ROUTES.get(mode, "Smart route: suggested by app")

    log = CommuteLog.objects.create(
        user=request.user,
        mode=mode,
        distance_km=distance_km,
        duration_minutes=payload.get("duration_minutes"),
        route_label=route_label,
        reliability_proof=payload.get("reliability_proof", ""),
        eco_scan_bonus=eco_scan_bonus,
        carbon_kg=carbon,
    )

    headline, change = _weekly_change(request.user)

    return Response(
        {
            "headline": headline,
            "smart_route": route_label,
            "eco_scan_hint": _eco_scan_hint(mode, eco_scan_bonus),
            "log": CommuteLogSerializer(log).data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_commute_logs(request):
    logs = CommuteLog.objects.filter(user=request.user)
    return Response(CommuteLogSerializer(logs, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def travel_summary(request):
    logs = CommuteLog.objects.filter(user=request.user)
    total_carbon = logs.aggregate(total=models.Sum("carbon_kg")).get("total") or 0
    headline, change = _weekly_change(request.user)

    mode_breakdown = (
        logs.values("mode")
        .annotate(distance=models.Sum("distance_km"), carbon=models.Sum("carbon_kg"))
        .order_by("mode")
    )

    return Response(
        {
            "headline": headline,
            "total_trips": logs.count(),
            "total_carbon_kg": round(total_carbon, 2),
            "mode_breakdown": list(mode_breakdown),
            "change_percent": change,
        }
    )
