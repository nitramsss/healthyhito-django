from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    bmi = models.FloatField()
    allergies = models.CharField(max_length=64) # Should be null


class UserHistory(models.Model):
    date = models.DateField(auto_now_add=True, null=True)
    meal_name = models.CharField(max_length=64)
    calories = models.FloatField()
    cuisine = models.CharField(max_length=64)
    meal_type = models.CharField(max_length=64)
    restriction = models.CharField(max_length=64)
    protein_source = models.CharField(max_length=64)
    cooking_time = models.FloatField()    
    budget = models.FloatField()    