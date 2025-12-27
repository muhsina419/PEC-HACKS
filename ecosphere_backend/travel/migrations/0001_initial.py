# Generated manually for EcoMiles travel tracking
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CommuteLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "mode",
                    models.CharField(
                        choices=[
                            ("bike", "Bike"),
                            ("bus_metro", "Bus/Metro"),
                            ("petrol", "Petrol/ICE"),
                            ("ev", "Electric Vehicle"),
                        ],
                        max_length=20,
                    ),
                ),
                ("distance_km", models.FloatField()),
                ("duration_minutes", models.PositiveIntegerField(blank=True, null=True)),
                ("route_label", models.CharField(blank=True, max_length=120)),
                ("reliability_proof", models.URLField(blank=True)),
                ("eco_scan_bonus", models.BooleanField(default=False)),
                ("carbon_kg", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
