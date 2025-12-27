from django.db import models

# Create your models here.
from django.db import models
from users.models import User

class EcoScan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    packaging_type = models.CharField(max_length=50)
    carbon_value = models.FloatField()
    scanned_at = models.DateTimeField(auto_now_add=True)


class EcoMiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transport_type = models.CharField(max_length=50)
    distance_km = models.FloatField()
    carbon_emission = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class EcoWatt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appliance = models.CharField(max_length=100)
    watt = models.IntegerField()
    hours_used = models.FloatField()
    carbon_output = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)


class EcoCycle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    disposal_type = models.CharField(max_length=50)
    eco_points = models.IntegerField()
    status = models.CharField(max_length=30)
