from django.conf import settings
from django.db import models


class ElectricityBill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # OCR extracted
    meter_number = models.CharField(max_length=50, null=True, blank=True)
    reading_current = models.FloatField()
    reading_previous = models.FloatField()
    units_consumed = models.FloatField()
    bill_amount = models.FloatField(default=0, null=True, blank=True)

    # User confirmation
    user_confirmed_units = models.FloatField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    # Carbon
    carbon_kg = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)


class HomeEnergyAssessment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill = models.ForeignKey(
        ElectricityBill, on_delete=models.SET_NULL, null=True, blank=True
    )
    total_carbon_kg = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class HomeApplianceUsage(models.Model):
    assessment = models.ForeignKey(
        HomeEnergyAssessment, related_name="appliances", on_delete=models.CASCADE
    )
    appliance_name = models.CharField(max_length=100)
    wattage = models.FloatField()
    star_rating = models.PositiveIntegerField()
    hours_per_day = models.FloatField()
    carbon_kg = models.FloatField()
    suggestion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
