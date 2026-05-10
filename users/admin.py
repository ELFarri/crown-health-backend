from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'age', 'gender', 'goal', 'activity_level']
    list_filter = ['gender', 'goal', 'activity_level']
    search_fields = ['name', 'email']