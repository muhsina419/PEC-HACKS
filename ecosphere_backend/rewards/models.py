from django.db import models

# Create your models here.
from django.db import models
from users.models import User

class Reward(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    level = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
