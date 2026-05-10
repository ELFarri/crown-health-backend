# nutrition/models.py - إضافة ForeignKey صحيح
from django.db import models
from users.models import CustomUser

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'إفطار'),
        ('lunch', 'غداء'),
        ('dinner', 'عشاء'),
        ('snack', 'وجبة خفيفة'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calories = models.IntegerField()
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"