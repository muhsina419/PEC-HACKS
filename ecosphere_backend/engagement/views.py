from datetime import timedelta
from typing import Optional

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rewards.models import Reward
from travel.models import CommuteLog
from waste.models import EcoCycleItem
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
from .serializers import (
    BadgeAwardSerializer,
    CommunityEventSerializer,
    CommunityGroupSerializer,
    EcoShopRecommendationSerializer,
    HabitReminderSerializer,
    LeaderboardEntrySerializer,
    ParticipationSerializer,
    RewardSummarySerializer,
    ScoreSnapshotSerializer,
    WasteReportSerializer,
    WasteReportUpdateSerializer,
)
from users.models import User


def _next_weekly_refresh():
    today = timezone.now().date()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    return today + timedelta(days=days_until_monday)


def _next_monthly_refresh():
    today = timezone.now().date()
    first_next_month = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
    return first_next_month


def _rank_for_scope(user, queryset):
    total = queryset.count()
    if total == 0:
        return 0, 0, 0
    higher = queryset.filter(eco_score__gt=user.eco_score).count()
    rank = higher + 1
    percentile = round((1 - higher / total) * 100, 1)
    return rank, percentile, total


def _seed_groups(user_city: Optional[str]):
    if CommunityGroup.objects.exists():
        return
    campus = CommunityGroup.objects.create(
        name="Campus EcoCircle",
        city=user_city or "Local",
        category="campus",
        description="Student-led cleanup drives and repair cafes.",
        invite_code="CAMPUS10",
    )
    city = CommunityGroup.objects.create(
        name="City Green Walks",
        city=user_city or "Local",
        category="community",
        description="Weekend plogging and park restoration meetups.",
        invite_code="CITY12",
    )

    CommunityEvent.objects.create(
        group=campus,
        title="Hostel e-waste drive",
        description="Drop chargers and gadgets for certified recycling.",
        location="Campus quad",
        starts_at=timezone.now() + timedelta(days=3),
        points_reward=25,
        carbon_focus="e-waste",
    )
    CommunityEvent.objects.create(
        group=city,
        title="Lakeside cleanup walk",
        description="Join neighbors for a 5km plogging loop.",
        location=f"{user_city or 'Local'} lakeside",
        starts_at=timezone.now() + timedelta(days=5),
        points_reward=30,
        carbon_focus="litter",
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    period = request.query_params.get("period", ScoreSnapshot.PERIOD_WEEKLY)
    user = request.user

    global_rank, global_percentile, global_total = _rank_for_scope(user, User.objects.all())
    if user.city:
        city_qs = User.objects.filter(city__iexact=user.city)
        city_rank, city_percentile, city_total = _rank_for_scope(user, city_qs)
    else:
        city_rank, city_percentile, city_total = None, None, 0

    locked_until = _next_weekly_refresh() if period == ScoreSnapshot.PERIOD_WEEKLY else _next_monthly_refresh()
    snapshot = ScoreSnapshot.objects.create(
        user=user,
        period=period,
        scope=ScoreSnapshot.SCOPE_GLOBAL,
        score_value=user.eco_score,
        percentile=global_percentile,
        rank=global_rank,
        locked_until=locked_until,
    )

    Reward.objects.get_or_create(user=user, defaults={"level": "Starter"})
    reward = Reward.objects.get(user=user)

    top_global = User.objects.all().order_by("-eco_score")[:10]
    leaderboard_entries = LeaderboardEntrySerializer(top_global, many=True).data

    payload = {
        "headline": f"You’re Top {global_percentile}% globally" if global_percentile else "Start logging to join the leaderboard",
        "city_headline": None if city_percentile is None else f"You’re Top {city_percentile}% in {user.city} this week",
        "score_locked_until": locked_until,
        "global_rank": global_rank,
        "city_rank": city_rank,
        "global_total": global_total,
        "city_total": city_total,
        "entries": leaderboard_entries,
        "reward": RewardSummarySerializer(reward).data,
        "snapshot": ScoreSnapshotSerializer(snapshot).data,
        "tips": [
            "Log low-carbon commutes to climb this week’s EcoRank.",
            "Scan EV or cycle receipts to lock in bonus points.",
            "Join a local EcoCircle event to boost your consistency streak.",
        ],
    }

    return Response(payload)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def groups(request):
    _seed_groups(request.user.city)
    qs = CommunityGroup.objects.all()
    if request.query_params.get("city"):
        qs = qs.filter(city__iexact=request.query_params["city"])
    serializer = CommunityGroupSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_group(request):
    group = get_object_or_404(CommunityGroup, pk=request.data.get("group"))
    membership, created = CommunityMembership.objects.get_or_create(user=request.user, group=group)
    if created:
        note = "Joined successfully"
    else:
        note = "Already a member"
    return Response({"message": note})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def events(request):
    _seed_groups(request.user.city)
    qs = CommunityEvent.objects.all()
    group_id = request.query_params.get("group")
    if group_id:
        qs = qs.filter(group_id=group_id)
    serializer = CommunityEventSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rsvp_event(request):
    serializer = ParticipationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    event = get_object_or_404(CommunityEvent, pk=serializer.validated_data["event"].id)
    participation, _ = EventParticipation.objects.update_or_create(
        user=request.user,
        event=event,
        defaults={
            "status": serializer.validated_data.get("status"),
            "proof_url": serializer.validated_data.get("proof_url", ""),
            "points_awarded": event.points_reward if serializer.validated_data.get("status") == EventParticipation.STATUS_ATTENDED else 0,
        },
    )

    reward, _ = Reward.objects.get_or_create(user=request.user, defaults={"level": "Starter"})
    reward.total_points += participation.points_awarded
    reward.save()

    return Response(
        {
            "message": "Attendance recorded" if participation.status == EventParticipation.STATUS_ATTENDED else "RSVP saved",
            "participation": ParticipationSerializer(participation).data,
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_report(request):
    serializer = WasteReportSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    report = WasteReport.objects.create(user=request.user, **serializer.validated_data)
    return Response(
        {
            "message": "Report submitted — verification pending",
            "report": WasteReportSerializer(report).data,
            "next_steps": "We’ll verify the photo and award EcoPoints if confirmed.",
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_reports(request):
    reports = WasteReport.objects.filter(user=request.user)
    return Response(WasteReportSerializer(reports, many=True).data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def verify_report(request, pk):
    if not request.user.is_staff:
        return Response({"detail": "Only moderators can verify"}, status=status.HTTP_403_FORBIDDEN)

    report = get_object_or_404(WasteReport, pk=pk)
    serializer = WasteReportUpdateSerializer(report, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    updated = serializer.save()
    if updated.status == WasteReport.STATUS_VERIFIED:
        updated.points_awarded = updated.points_awarded or 35
        updated.verified_at = updated.verified_at or timezone.now()
        updated.save()
        reward, _ = Reward.objects.get_or_create(user=updated.user, defaults={"level": "Starter"})
        reward.total_points += updated.points_awarded
        reward.save()
    return Response(WasteReportSerializer(updated).data)


BADGE_DEFINITIONS = [
    {
        "slug": "reuse-hero",
        "title": "Reuse Hero",
        "category": "waste",
        "description": "Logged 3+ reuse/refill actions in EcoCycle.",
        "icon": "♻️",
    },
    {
        "slug": "zero-waste-week",
        "title": "Zero Waste Week",
        "category": "waste",
        "description": "No landfill disposals in the last 7 days.",
        "icon": "🧭",
    },
    {
        "slug": "local-shopper",
        "title": "Local Shopper",
        "category": "shopping",
        "description": "High score with local city activity — keep it up!",
        "icon": "🛍️",
    },
    {
        "slug": "consistent-logger",
        "title": "Consistent Logger",
        "category": "habits",
        "description": "Logged 7+ commutes or scans this week.",
        "icon": "📅",
    },
]


def _ensure_badges():
    for badge in BADGE_DEFINITIONS:
        Badge.objects.get_or_create(slug=badge["slug"], defaults=badge)


def _award_badge(user, slug, metric_value=None, note=""):
    badge = Badge.objects.get(slug=slug)
    award, created = BadgeAward.objects.get_or_create(user=user, badge=badge)
    if created:
        award.metric_value = metric_value
        award.note = note
        award.save()
    return created, award


def _check_badges(user):
    _ensure_badges()

    reused_count = EcoCycleItem.objects.filter(user=user, disposal_status=EcoCycleItem.STATUS_REUSED).count()
    if reused_count >= 3:
        _award_badge(user, "reuse-hero", metric_value=reused_count, note="Refilled containers multiple times")

    last_week = timezone.now().date() - timedelta(days=7)
    landfill = EcoCycleItem.objects.filter(
        user=user,
        disposal_status=EcoCycleItem.STATUS_LANDFILL,
        created_at__date__gte=last_week,
    ).count()
    if landfill == 0:
        _award_badge(user, "zero-waste-week", note="Kept landfill at zero this week")

    if user.city:
        city_peers = User.objects.filter(city__iexact=user.city).count() or 1
        if (user.eco_score or 0) >= 50 and city_peers >= 1:
            _award_badge(user, "local-shopper", metric_value=user.eco_score, note="High local eco-score")

    week_ago = timezone.now() - timedelta(days=7)
    commute_count = CommuteLog.objects.filter(user=user, created_at__gte=week_ago).count()
    if commute_count >= 7:
        _award_badge(user, "consistent-logger", metric_value=commute_count, note="Daily travel logs")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def badges(request):
    _check_badges(request.user)
    awards = BadgeAward.objects.filter(user=request.user).select_related("badge")
    return Response(BadgeAwardSerializer(awards, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_reminder(request):
    serializer = HabitReminderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    reminder = HabitReminder.objects.create(
        user=request.user,
        **serializer.validated_data,
        streak_days=serializer.validated_data.get("streak_days", 0),
    )
    return Response(HabitReminderSerializer(reminder).data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reminders(request):
    qs = HabitReminder.objects.filter(user=request.user)
    return Response(
        {
            "due": HabitReminderSerializer(qs.filter(next_trigger_at__lte=timezone.now(), active=True), many=True).data,
            "scheduled": HabitReminderSerializer(qs, many=True).data,
            "suggestion": "Enable expiry and disposal nudges to protect your EcoScore streak.",
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def eco_shop(request):
    recommendations = EcoShopRecommendation.objects.filter(user=request.user)
    if not recommendations.exists():
        default_recs = [
            {
                "product_name": "LED bulbs (4-pack)",
                "category": "home",
                "carbon_saving_kg_month": 4.2,
                "offer_text": "10% partner cashback",
                "reason": "Swap from CFL to LED to cut EcoWatt usage.",
            },
            {
                "product_name": "Refillable cleaning kit",
                "category": "home",
                "carbon_saving_kg_month": 2.1,
                "offer_text": "Free first refill",
                "reason": "Reduce plastic waste and score Reuse Hero progress.",
            },
            {
                "product_name": "Local farm veggie box",
                "category": "food",
                "carbon_saving_kg_month": 5.3,
                "offer_text": "City-only delivery",
                "reason": "Cut import miles and qualify for Local Shopper.",
            },
        ]
        for rec in default_recs:
            EcoShopRecommendation.objects.create(user=request.user, **rec)
        recommendations = EcoShopRecommendation.objects.filter(user=request.user)

    return Response(
        {
            "headline": "EcoShop picks ready",
            "recommendations": EcoShopRecommendationSerializer(recommendations, many=True).data,
            "tip": "Switch to refill packs to save 1.1kg CO₂e/month and unlock cashback.",
        }
    )
