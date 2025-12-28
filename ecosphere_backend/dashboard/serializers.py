from rest_framework import serializers

from .models import CarbonWallet


class CarbonWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonWallet
        fields = [
            "total_carbon_kg",
            "eco_score",
            "breakdown",
            "updated_at",
        ]


class CarbonSummarySerializer(serializers.Serializer):
    wallet = CarbonWalletSerializer()
    headline = serializers.CharField()
    tips = serializers.ListField(child=serializers.CharField())
