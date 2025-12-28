from django.conf import settings
from django.db import models
from django.utils import timezone


class InventoryItem(models.Model):
    product_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100)
    packaging = models.CharField(max_length=255)
    packaging_tags = models.JSONField(default=list)
    eco_score = models.IntegerField()
    image = models.URLField(blank=True)
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def days_left(self):
        return (self.expiry_date - timezone.now().date()).days


class UserAction(models.Model):
    ACTION_CHOICES = [
        ("recycled", "Recycled"),
        ("reused", "Reused"),
        ("donated", "Donated"),
        ("discarded", "Discarded"),
    ]

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name="actions"
    )

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    points_awarded = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class FoodImpact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    packaging_type = models.CharField(max_length=100)
    distance_km = models.FloatField()
    carbon_kg = models.FloatField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
