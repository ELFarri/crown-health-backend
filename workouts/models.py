from django.db import models
from users.models import CustomUser

class Workout(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    
    def __str__(self):
        return self.name

class UserWorkout(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration = models.IntegerField()