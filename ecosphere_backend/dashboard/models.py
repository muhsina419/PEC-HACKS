from django.conf import settings
from django.db import models
from django.db.models import Sum

from electricity.models import HomeEnergyAssessment
from food.models import EcoPlateEntry
from inventory.models import FoodImpact
from travel.models import CommuteLog
from waste.models import EcoCycleItem


class CarbonWallet(models.Model):
    """Aggregate carbon footprint and EcoScore for a user."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_carbon_kg = models.FloatField(default=0)
    eco_score = models.IntegerField(default=100)
    breakdown = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__id"]

    @staticmethod
    def _safe_sum(qs, field):
        return qs.aggregate(total=Sum(field)).get("total") or 0

    def refresh_from_sources(self):
        travel_carbon = self._safe_sum(
            CommuteLog.objects.filter(user=self.user), "carbon_kg"
        )
        home_energy_carbon = self._safe_sum(
            HomeEnergyAssessment.objects.filter(user=self.user), "total_carbon_kg"
        )
        food_plate_carbon = self._safe_sum(
            EcoPlateEntry.objects.filter(user=self.user), "carbon_kg"
        )
        packaged_food_carbon = self._safe_sum(
            FoodImpact.objects.filter(user=self.user), "carbon_kg"
        )
        waste_score = self._safe_sum(
            EcoCycleItem.objects.filter(user=self.user), "score"
        )

        total_carbon = travel_carbon + home_energy_carbon + food_plate_carbon + packaged_food_carbon

        # EcoScore: start from 100, penalize direct emissions, then reward positive waste actions.
        eco_score = max(0, round(100 - total_carbon)) + int(waste_score)

        self.total_carbon_kg = round(total_carbon, 2)
        self.eco_score = eco_score
        self.breakdown = {
            "travel_carbon_kg": round(travel_carbon, 2),
            "home_energy_carbon_kg": round(home_energy_carbon, 2),
            "food_carbon_kg": round(food_plate_carbon + packaged_food_carbon, 2),
            "waste_score": int(waste_score),
        }
        self.save()
        return self
