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
            name='EcoPlateEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_type', models.CharField(max_length=100)),
                ('packaging_type', models.CharField(choices=[('plastic', 'Plastic'), ('paper', 'Paper'), ('compostable', 'Compostable'), ('reusable', 'Reusable'), ('other', 'Other')], max_length=20)),
                ('delivery_mode', models.CharField(choices=[('bike', 'Bike'), ('ev', 'Electric Vehicle'), ('car', 'Car'), ('other', 'Other')], max_length=20)),
                ('distance_km', models.FloatField()),
                ('carbon_kg', models.FloatField()),
                ('impact_label', models.CharField(max_length=20)),
                ('suggestion', models.CharField(max_length=255)),
                ('bill_reference', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
