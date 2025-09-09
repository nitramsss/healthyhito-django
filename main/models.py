from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    age = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)
    bmi = models.FloatField(null=True)


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=64, null=True)
    calories = models.FloatField(null=True)
    description = models.TextField(null=True)
    ingredients = models.TextField(null=True)
    steps = models.TextField(null=True)
    duration = models.CharField(max_length=64, null=True)    
    budget = models.CharField(max_length=64, null=True)  

    def __str__(self):
        return f'user: {self.user}\ndata: {self.date}\
            \ntitle: {self.title}\ncalories: {self.calories}\
            \ndescription: {self.description}\ningredients: {self.ingredients}\
            \nsteps: {self.steps}\nduration: {self.duration}\
            \nbudget: {self.budget}'