from rest_framework import serializers

from .models import ElectricityBill

EMISSION_FACTOR = 0.82  # kg CO2 per unit


class ElectricityBillSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectricityBill
        fields = [
            "id",
            "meter_number",
            "reading_previous",
            "reading_current",
            "units_consumed",
            "bill_amount",
            "user_confirmed_units",
            "verified",
            "carbon_kg",
            "created_at",
        ]
        read_only_fields = ["units_consumed", "verified", "carbon_kg", "created_at"]

    def create(self, validated_data):
        reading_previous = validated_data["reading_previous"]
        reading_current = validated_data["reading_current"]
        units = reading_current - reading_previous
        carbon = round(units * EMISSION_FACTOR, 2)

        validated_data.setdefault("user_confirmed_units", units)
        validated_data["units_consumed"] = units
        validated_data["carbon_kg"] = carbon

        user = self.context["request"].user
        return ElectricityBill.objects.create(user=user, **validated_data)
