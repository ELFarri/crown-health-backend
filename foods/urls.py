# foods/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.food_list, name='food_list'),
    path('search/', views.food_search, name='food_search'),

]