from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from electricity.models import HomeEnergyAssessment
from travel.models import CommuteLog

from .models import CarbonWallet
from .serializers import CarbonSummarySerializer, CarbonWalletSerializer


class CarbonFootprintView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_wallet(self, user):
        wallet, _ = CarbonWallet.objects.get_or_create(user=user)
        wallet.refresh_from_sources()
        return wallet

    def get(self, request):
        wallet = self.get_wallet(request.user)

        breakdown = wallet.breakdown
        biggest_area = max(
            [
                ("Travel", breakdown.get("travel_carbon_kg", 0)),
                ("Home energy", breakdown.get("home_energy_carbon_kg", 0)),
                ("Food", breakdown.get("food_carbon_kg", 0)),
            ],
            key=lambda item: item[1],
        )[0]

        trend = CommuteLog.objects.filter(user=request.user).count()
        headline = (
            f"Your {biggest_area} footprint is leading current emissions"
            if wallet.total_carbon_kg
            else "Great job — no emissions recorded yet"
        )
        if trend >= 7:
            headline += " and weekly travel logs are keeping you consistent"

        tips = []
        if breakdown.get("home_energy_carbon_kg", 0) > 0:
            latest_assessment = (
                HomeEnergyAssessment.objects.filter(user=request.user)
                .order_by("-created_at")
                .first()
            )
            if latest_assessment:
                tips.append(
                    "Review EcoWatt suggestions in your last assessment to drop heavy appliances."
                )
        if breakdown.get("travel_carbon_kg", 0) > breakdown.get("food_carbon_kg", 0):
            tips.append("Switch more trips to bike/metro to unlock EcoMiles bonuses.")
        if breakdown.get("waste_score", 0) <= 0:
            tips.append("Log disposal proof to convert waste into positive EcoScore.")

        payload = {
            "wallet": CarbonWalletSerializer(wallet).data,
            "headline": headline,
            "tips": tips,
        }
        return Response(CarbonSummarySerializer(payload).data)
