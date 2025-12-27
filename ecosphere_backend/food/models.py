from django.conf import settings
from django.db import models


class EcoPlateEntry(models.Model):
    """Record of a packaged/parcel meal scan with impact details."""

    PACKAGING_CHOICES = [
        ("plastic", "Plastic"),
        ("paper", "Paper"),
        ("compostable", "Compostable"),
        ("reusable", "Reusable"),
        ("other", "Other"),
    ]

    DELIVERY_MODES = [
        ("bike", "Bike"),
        ("ev", "Electric Vehicle"),
        ("car", "Car"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=100)
    packaging_type = models.CharField(max_length=20, choices=PACKAGING_CHOICES)
    delivery_mode = models.CharField(max_length=20, choices=DELIVERY_MODES)
    distance_km = models.FloatField()
    carbon_kg = models.FloatField()
    impact_label = models.CharField(max_length=20)
    suggestion = models.CharField(max_length=255)
    bill_reference = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
