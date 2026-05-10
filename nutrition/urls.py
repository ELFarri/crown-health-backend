from django.urls import path
from . import views

urlpatterns = [
    path('meals/', views.meals_list),
    path('meals/add/', views.add_meal),
]