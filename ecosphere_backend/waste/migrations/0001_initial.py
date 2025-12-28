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
            name='EcoCycleItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('packaging', models.CharField(blank=True, max_length=255)),
                ('expiry_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('disposal_status', models.CharField(choices=[('recycled', 'Recycled'), ('reused', 'Reused / Refilled'), ('composted', 'Composted'), ('landfill', 'Landfill'), ('none', 'No update')], default='none', max_length=20)),
                ('disposal_proof_url', models.URLField(blank=True)),
                ('disposal_notes', models.TextField(blank=True)),
                ('disposal_logged_at', models.DateTimeField(blank=True, null=True)),
                ('score', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
