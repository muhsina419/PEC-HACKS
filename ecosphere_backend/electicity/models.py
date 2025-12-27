from django.db import models

# Create your models here.
class ElectricityBill(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    
    # OCR extracted
    meter_number = models.CharField(max_length=50, null=True)
    reading_current = models.FloatField()
    reading_previous = models.FloatField()
    units_consumed = models.FloatField()
    bill_amount = models.FloatField()

    # User confirmation
    user_confirmed_units = models.FloatField()
    verified = models.BooleanField(default=False)

    # Carbon
    carbon_kg = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
