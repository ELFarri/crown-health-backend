from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    
    # 👇 إصلاح الـ CHOICES هنا
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    GOAL_CHOICES = [
        ('loss', 'Weight Loss'),
        ('gain', 'Weight Gain'),
        ('maintain', 'Maintain Weight'),
    ]
    
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Light Exercise'),
        ('moderate', 'Moderate Exercise'),
        ('active', 'Active'),
        ('very_active', 'Very Active'),
    ]
    
    # الحقول مع الـ choices الصحيحة
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, blank=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, blank=True)

    def __str__(self):
        return self.username