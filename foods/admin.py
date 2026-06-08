# ===================================================================================================================
# FILE: foods/admin.py
# PURPOSE: Registers the Food model with Django's Admin Panel.
#          Gives admins a powerful browser-based interface to manage the food ingredient database:
#          add new foods, edit nutritional values, filter by category, and search by name/brand.
#
# HOW TO ACCESS:
#   1. python manage.py runserver → start the server
#   2. Go to http://127.0.0.1:8000/admin/
#   3. Log in with superuser credentials
#   4. Click "Foods" to manage the food catalogue
#
# WHY THIS MATTERS:
#   The Food database is the ingredient library that powers the meal logging autocomplete.
#   Admins use this panel to curate, verify, and expand the food catalogue without writing any SQL.
# ===================================================================================================================

from django.contrib import admin  # Django's admin registration system
from .models import Food          # Import the Food model from foods/models.py


@admin.register(Food)             # Decorator: registers Food with the admin site using FoodAdmin as the config
class FoodAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for the Food model.
    Controls list display columns, filters, search, pagination, and form field ordering.
    """

    # list_display: defines which columns appear in the Food list table in the admin panel.
    # Each string = a field name from the Food model.
    # Example row: | Grilled Chicken | Natural | proteins | 165 | 31.0 | ✓ |
    list_display = ['name', 'brand', 'category', 'calories', 'protein', 'is_verified']

    # list_filter: sidebar filter panel with clickable filter buttons.
    # 'category'   → filter by food group (vegetables, proteins, carbs, etc.)
    # 'is_verified' → filter verified vs. unverified foods
    # 'created_at' → filter by creation date (Today, Past 7 days, This month, This year)
    list_filter = ['category', 'is_verified', 'created_at']

    # search_fields: activates the search bar at the top of the admin list.
    # Django runs a SQL ILIKE query on both 'name' and 'brand' columns simultaneously.
    # Example: searching "natural" finds all foods where name OR brand contains "natural"
    search_fields = ['name', 'brand']

    # list_per_page: number of food records shown per page in the admin list view.
    # Default Django value is 100; 20 is more readable for food data with many columns.
    list_per_page = 20

    # ordering: default sort order for the admin list view.
    # ['name'] → alphabetical ascending (A → Z) by food name
    ordering = ['name']

    # fields: controls the order and layout of input fields in the Add/Edit food form.
    # Only fields listed here will appear in the admin create/edit form.
    # Fields are displayed in the exact order listed below.
    fields = [
        'name',         # Food name input (required)
        'brand',        # Brand name input (optional)
        'category',     # Category dropdown (vegetables, fruits, proteins, etc.)
        'serving_size', # Serving size text field (e.g. "100g", "1 cup")
        'calories',     # Calorie input in kcal per serving
        'protein',      # Protein in grams
        'carbs',        # Carbohydrates in grams
        'fat',          # Fat in grams
        'fiber',        # Dietary fiber in grams
        'sugar',        # Sugar content in grams
        'description',  # Optional text description of the food
        'is_verified',  # Checkbox: marks food as verified by admin (trusted data)
    ]