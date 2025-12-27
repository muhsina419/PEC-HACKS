from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import EcoCycleItem
from .serializers import EcoCycleDisposalSerializer, EcoCycleItemSerializer


def _alert_stage(item: EcoCycleItem) -> str:
    days_left = item.days_left()
    if days_left < -1:
        return "overdue"
    if days_left <= -1:
        return "grace"
    if days_left == 0:
        return "expiry"
    if days_left <= 3:
        return "3d"
    if days_left <= 7:
        return "7d"
    return "scheduled"


def _alert_message(item: EcoCycleItem) -> str:
    stage = _alert_stage(item)
    if stage == "7d":
        return "7-day reminder: plan reuse or recycling to avoid expiry waste."
    if stage == "3d":
        return "3-day alert: log a disposal plan to protect your EcoScore."
    if stage == "expiry":
        return "Expires today — update the EcoCycle log to avoid a penalty."
    if stage == "grace":
        return "24h grace: add disposal proof to prevent an automatic -10."
    if stage == "overdue":
        return "Past grace window — log a status to recover lost points."
    return "Scheduled in advance — you can still switch to reusable options."


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_item(request):
    serializer = EcoCycleItemSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    entry = EcoCycleItem.objects.create(
        user=request.user,
        item_name=serializer.validated_data["item_name"],
        packaging=serializer.validated_data.get("packaging", ""),
        expiry_date=serializer.validated_data["expiry_date"],
    )

    payload = EcoCycleItemSerializer(entry).data
    payload["alert_message"] = _alert_message(entry)
    return Response(payload, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_items(request):
    items = EcoCycleItem.objects.filter(user=request.user)
    data = []
    for item in items:
        serialized = EcoCycleItemSerializer(item).data
        serialized["alert_message"] = _alert_message(item)
        data.append(serialized)
    return Response(data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_disposal(request, pk):
    item = get_object_or_404(EcoCycleItem, pk=pk, user=request.user)
    serializer = EcoCycleDisposalSerializer(instance=item, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    updated = serializer.save()
    payload = EcoCycleItemSerializer(updated).data
    payload["alert_message"] = _alert_message(updated)
    payload["headline"] = _disposal_headline(updated)
    return Response(payload)


def _disposal_headline(item: EcoCycleItem) -> str:
    if item.disposal_status == EcoCycleItem.STATUS_RECYCLED:
        proof = "with proof" if item.disposal_proof_url else "(no proof)"
        return f"Recycled {proof} → +{item.score} EcoPoints"
    if item.disposal_status == EcoCycleItem.STATUS_REUSED:
        return f"Reused / Refilled → +{item.score} EcoPoints"
    if item.disposal_status == EcoCycleItem.STATUS_COMPOSTED:
        return f"Composted → +{item.score} EcoPoints"
    if item.disposal_status == EcoCycleItem.STATUS_LANDFILL:
        return "Landfill logged — no EcoPoints added"
    return "No update — log disposal to avoid penalties"


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def alerts(request):
    today = timezone.now().date()
    upcoming = EcoCycleItem.objects.filter(user=request.user, expiry_date__lte=today + timedelta(days=7))
    data = []
    for item in upcoming:
        serialized = EcoCycleItemSerializer(item).data
        serialized["alert_stage"] = _alert_stage(item)
        serialized["alert_message"] = _alert_message(item)
        serialized["headline"] = _disposal_headline(item)
        data.append(serialized)
    return Response(
        {
            "count": len(data),
            "items": data,
            "summary": _alerts_summary(data),
        }
    )


def _alerts_summary(data):
    if not data:
        return "All clear — no items expiring in the next week."
    urgent = [d for d in data if d["alert_stage"] in {"expiry", "grace", "overdue"}]
    if urgent:
        return f"{len(urgent)} items need action today to protect your EcoScore."
    soon = [d for d in data if d["alert_stage"] in {"3d", "7d"}]
    return f"{len(soon)} items are approaching expiry — plan reuse or compost now."
