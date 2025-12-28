from django.utils import timezone
from rest_framework import serializers

from .models import EcoCycleItem


class EcoCycleItemSerializer(serializers.ModelSerializer):
    days_left = serializers.SerializerMethodField()
    alert_stage = serializers.SerializerMethodField()
    projected_score = serializers.SerializerMethodField()

    class Meta:
        model = EcoCycleItem
        fields = [
            "id",
            "item_name",
            "packaging",
            "expiry_date",
            "disposal_status",
            "disposal_proof_url",
            "disposal_notes",
            "disposal_logged_at",
            "score",
            "days_left",
            "alert_stage",
            "projected_score",
            "created_at",
        ]
        read_only_fields = [
            "disposal_logged_at",
            "score",
            "days_left",
            "alert_stage",
            "projected_score",
            "created_at",
        ]

    def get_days_left(self, obj: EcoCycleItem) -> int:
        return obj.days_left()

    def get_alert_stage(self, obj: EcoCycleItem) -> str:
        days_left = obj.days_left()
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

    def get_projected_score(self, obj: EcoCycleItem) -> int:
        return obj.calculate_score()


class EcoCycleDisposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoCycleItem
        fields = ["disposal_status", "disposal_proof_url", "disposal_notes"]

    def validate_disposal_status(self, value):
        if value == EcoCycleItem.STATUS_NONE:
            raise serializers.ValidationError("Use a disposal outcome to update the log.")
        return value

    def update(self, instance: EcoCycleItem, validated_data):
        instance.disposal_status = validated_data.get("disposal_status", instance.disposal_status)
        instance.disposal_proof_url = validated_data.get(
            "disposal_proof_url", instance.disposal_proof_url
        )
        instance.disposal_notes = validated_data.get("disposal_notes", instance.disposal_notes)
        instance.disposal_logged_at = timezone.now()
        instance.save()
        return instance
