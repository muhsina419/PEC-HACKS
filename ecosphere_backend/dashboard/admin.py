from django.contrib import admin

from .models import CarbonWallet


@admin.register(CarbonWallet)
class CarbonWalletAdmin(admin.ModelAdmin):
    list_display = ("user", "total_carbon_kg", "eco_score", "updated_at")
    search_fields = ("user__phone_number", "user__email")
    readonly_fields = ("updated_at",)
