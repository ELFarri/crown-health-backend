from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.workouts_list),
    path('workouts/add/', views.add_workout),
]