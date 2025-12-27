from django.contrib.auth import get_user_model
from rest_framework import serializers

from rewards.models import Reward
from .models import (
    Badge,
    BadgeAward,
    CommunityEvent,
    CommunityGroup,
    CommunityMembership,
    EcoShopRecommendation,
    EventParticipation,
    HabitReminder,
    ScoreSnapshot,
    WasteReport,
)

User = get_user_model()


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "city", "eco_score"]


class ScoreSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreSnapshot
        fields = [
            "id",
            "period",
            "scope",
            "score_value",
            "percentile",
            "rank",
            "locked_until",
            "created_at",
        ]


class RewardSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ["total_points", "level", "updated_at"]


class CommunityGroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = CommunityGroup
        fields = [
            "id",
            "name",
            "city",
            "category",
            "description",
            "invite_code",
            "member_count",
            "is_member",
        ]

    def get_member_count(self, obj):
        return obj.member_count()

    def get_is_member(self, obj):
        user = self.context.get("request").user
        return obj.memberships.filter(user=user).exists()


class CommunityEventSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source="group.name", read_only=True)
    attendees = serializers.SerializerMethodField()

    class Meta:
        model = CommunityEvent
        fields = [
            "id",
            "group",
            "group_name",
            "title",
            "description",
            "location",
            "starts_at",
            "points_reward",
            "carbon_focus",
            "attendees",
        ]

    def get_attendees(self, obj):
        return obj.participations.count()


class ParticipationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source="event.title", read_only=True)

    class Meta:
        model = EventParticipation
        fields = [
            "id",
            "event",
            "event_title",
            "status",
            "proof_url",
            "points_awarded",
            "created_at",
        ]


class WasteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteReport
        fields = [
            "id",
            "title",
            "description",
            "photo_url",
            "location",
            "status",
            "points_awarded",
            "verified_at",
            "created_at",
        ]
        read_only_fields = ["status", "points_awarded", "verified_at", "created_at"]


class WasteReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteReport
        fields = ["status", "points_awarded", "verified_at"]


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ["id", "slug", "title", "category", "description", "icon"]


class BadgeAwardSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = BadgeAward
        fields = ["id", "badge", "awarded_at", "metric_value", "note"]


class HabitReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitReminder
        fields = [
            "id",
            "reminder_type",
            "message",
            "cadence_days",
            "next_trigger_at",
            "active",
            "streak_days",
            "last_triggered_at",
        ]
        read_only_fields = ["streak_days", "last_triggered_at"]


class EcoShopRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoShopRecommendation
        fields = [
            "id",
            "product_name",
            "category",
            "carbon_saving_kg_month",
            "offer_text",
            "reason",
            "created_at",
        ]
        read_only_fields = ["created_at"]
