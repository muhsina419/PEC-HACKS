# Generated manually by ChatGPT
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
            name="ElectricityBill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("meter_number", models.CharField(blank=True, max_length=50, null=True)),
                ("reading_current", models.FloatField()),
                ("reading_previous", models.FloatField()),
                ("units_consumed", models.FloatField()),
                ("bill_amount", models.FloatField(blank=True, default=0, null=True)),
                ("user_confirmed_units", models.FloatField(blank=True, null=True)),
                ("verified", models.BooleanField(default=False)),
                ("carbon_kg", models.FloatField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
