from django.contrib import admin

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

admin.site.register(
    [
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
    ]
)
