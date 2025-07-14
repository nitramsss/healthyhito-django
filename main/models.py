from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()
    allergies = models.CharField(max_length=64)
