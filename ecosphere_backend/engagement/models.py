from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class ScoreSnapshot(models.Model):
    PERIOD_WEEKLY = "weekly"
    PERIOD_MONTHLY = "monthly"
    PERIOD_CHOICES = [(PERIOD_WEEKLY, "Weekly"), (PERIOD_MONTHLY, "Monthly")]

    SCOPE_GLOBAL = "global"
    SCOPE_CITY = "city"
    SCOPE_CHOICES = [(SCOPE_GLOBAL, "Global"), (SCOPE_CITY, "City")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=16, choices=PERIOD_CHOICES)
    scope = models.CharField(max_length=16, choices=SCOPE_CHOICES)
    score_value = models.IntegerField(default=0)
    percentile = models.FloatField(default=0)
    rank = models.IntegerField(null=True, blank=True)
    locked_until = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class CommunityGroup(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, default="general")
    description = models.TextField(blank=True)
    invite_code = models.CharField(max_length=12, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def member_count(self):
        return self.memberships.count()

    class Meta:
        ordering = ["name"]


class CommunityMembership(models.Model):
    ROLE_MEMBER = "member"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [(ROLE_MEMBER, "Member"), (ROLE_ADMIN, "Admin")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")
        ordering = ["-joined_at"]


class CommunityEvent(models.Model):
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    starts_at = models.DateTimeField()
    points_reward = models.IntegerField(default=0)
    carbon_focus = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["starts_at"]


class EventParticipation(models.Model):
    STATUS_GOING = "going"
    STATUS_INTERESTED = "interested"
    STATUS_ATTENDED = "attended"
    STATUS_CHOICES = [
        (STATUS_GOING, "Going"),
        (STATUS_INTERESTED, "Interested"),
        (STATUS_ATTENDED, "Attended"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(CommunityEvent, on_delete=models.CASCADE, related_name="participations")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_GOING)
    proof_url = models.URLField(blank=True)
    points_awarded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")
        ordering = ["-created_at"]


class WasteReport(models.Model):
    STATUS_PENDING = "pending"
    STATUS_VERIFIED = "verified"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_VERIFIED, "Verified"),
        (STATUS_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    photo_url = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    points_awarded = models.IntegerField(default=0)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Badge(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=80)
    description = models.TextField()
    icon = models.CharField(max_length=10, default="🏅")

    class Meta:
        ordering = ["title"]


class BadgeAward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    metric_value = models.FloatField(null=True, blank=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("user", "badge")
        ordering = ["-awarded_at"]


class HabitReminder(models.Model):
    REMINDER_SCAN = "scan"
    REMINDER_DISPOSAL = "disposal"
    REMINDER_EXPIRY = "expiry"
    REMINDER_CUSTOM = "custom"
    REMINDER_CHOICES = [
        (REMINDER_SCAN, "Scan"),
        (REMINDER_DISPOSAL, "Disposal"),
        (REMINDER_EXPIRY, "Expiry"),
        (REMINDER_CUSTOM, "Custom"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_type = models.CharField(max_length=20, choices=REMINDER_CHOICES)
    message = models.CharField(max_length=200)
    cadence_days = models.PositiveIntegerField(default=1)
    next_trigger_at = models.DateTimeField()
    active = models.BooleanField(default=True)
    streak_days = models.PositiveIntegerField(default=0)
    last_triggered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["next_trigger_at"]


class EcoShopRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="eco_shop_recommendations")
    product_name = models.CharField(max_length=150)
    category = models.CharField(max_length=100, blank=True)
    carbon_saving_kg_month = models.FloatField(default=0)
    offer_text = models.CharField(max_length=150, blank=True)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
