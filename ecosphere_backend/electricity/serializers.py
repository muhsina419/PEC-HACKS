from rest_framework import serializers

from .models import ElectricityBill, HomeApplianceUsage, HomeEnergyAssessment

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


class ApplianceInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    wattage = serializers.FloatField()
    star_rating = serializers.IntegerField(min_value=1, max_value=5)
    hours_per_day = serializers.FloatField(min_value=0)


class HomeApplianceUsageSerializer(serializers.ModelSerializer):
    share_percent = serializers.SerializerMethodField()

    class Meta:
        model = HomeApplianceUsage
        fields = [
            "id",
            "appliance_name",
            "wattage",
            "star_rating",
            "hours_per_day",
            "carbon_kg",
            "share_percent",
            "suggestion",
            "created_at",
        ]

    def get_share_percent(self, obj):
        total = self.context.get("total_carbon", 0) or 0
        if total:
            return round((obj.carbon_kg / total) * 100, 1)
        return 0.0


class HomeEnergyAssessmentSerializer(serializers.ModelSerializer):
    appliances = serializers.SerializerMethodField()

    class Meta:
        model = HomeEnergyAssessment
        fields = ["id", "total_carbon_kg", "appliances", "created_at", "bill_id"]

    def get_appliances(self, obj):
        return HomeApplianceUsageSerializer(
            obj.appliances.all(),
            many=True,
            context={"total_carbon": obj.total_carbon_kg},
        ).data
