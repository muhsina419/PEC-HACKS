from rest_framework import serializers

from .models import EcoPlateEntry


class EcoPlateEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoPlateEntry
        fields = [
            "id",
            "meal_type",
            "packaging_type",
            "delivery_mode",
            "distance_km",
            "carbon_kg",
            "impact_label",
            "suggestion",
            "bill_reference",
            "created_at",
        ]
        read_only_fields = ["carbon_kg", "impact_label", "suggestion", "created_at"]
        extra_kwargs = {
            "bill_reference": {"required": False, "allow_blank": True},
        }
