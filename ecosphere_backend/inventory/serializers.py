from rest_framework import serializers
from .models import InventoryItem

class InventorySerializer(serializers.ModelSerializer):
    days_left = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "product_name",
            "brand",
            "category",
            "quantity",
            "packaging",
            "eco_score",
            "image",
            "expiry_date",
            "days_left"
        ]

    def get_days_left(self, obj):
        return (obj.expiry_date - obj.created_at.date()).days
