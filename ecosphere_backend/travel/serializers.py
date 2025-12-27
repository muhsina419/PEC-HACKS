from rest_framework import serializers

from .models import CommuteLog


class CommuteLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommuteLog
        fields = [
            "id",
            "mode",
            "distance_km",
            "duration_minutes",
            "route_label",
            "reliability_proof",
            "eco_scan_bonus",
            "carbon_kg",
            "created_at",
        ]
        read_only_fields = ["route_label", "carbon_kg", "created_at"]
        extra_kwargs = {
            "reliability_proof": {"required": False, "allow_blank": True},
            "duration_minutes": {"required": False, "allow_null": True},
            "eco_scan_bonus": {"required": False},
        }
