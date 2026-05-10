from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_api, name='register'),
    path('login/', views.login_api, name='login'),
    path('profile/', views.profile_api, name='profile'),
]