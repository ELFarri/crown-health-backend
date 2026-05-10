# foods/admin.py - انسخ والصق
from django.contrib import admin
from .models import Food

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'calories', 'protein', 'is_verified']
    list_filter = ['category', 'is_verified', 'created_at']
    search_fields = ['name', 'brand']
    list_per_page = 20
    ordering = ['name']
    
    # Fields في Add form
    fields = ['name', 'brand', 'category', 'serving_size', 'calories', 
              'protein', 'carbs', 'fat', 'fiber', 'sugar', 'description', 'is_verified']