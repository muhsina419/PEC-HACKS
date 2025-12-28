from django.conf import settings
from django.db import models


class CommuteLog(models.Model):
    """Daily commute entries with calculated carbon output."""

    MODE_CHOICES = [
        ("bike", "Bike"),
        ("bus_metro", "Bus/Metro"),
        ("petrol", "Petrol/ICE"),
        ("ev", "Electric Vehicle"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    distance_km = models.FloatField()
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    route_label = models.CharField(max_length=120, blank=True)
    reliability_proof = models.URLField(blank=True)
    eco_scan_bonus = models.BooleanField(default=False)
    carbon_kg = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
