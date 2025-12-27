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
