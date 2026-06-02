from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.workouts_list),
    path('history/', views.user_workout_history),
    path('history/clear/', views.clear_workout_history),
]