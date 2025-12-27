from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    eco_score = models.IntegerField(default=0)
    city = models.CharField(max_length=100, blank=True)
