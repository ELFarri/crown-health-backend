from django.contrib import admin
from .models import Workout, UserWorkout

admin.site.register(Workout)
admin.site.register(UserWorkout)