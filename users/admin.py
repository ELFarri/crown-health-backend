# ===================================================================================================================
# FILE: users/admin.py
# PURPOSE: Registers the CustomUser model with Django's ADMIN PANEL interface.
#          The Django admin panel (/admin/) is a built-in browser-based tool that allows
#          authorized staff members to view, create, edit, search, and delete database records
#          without writing any SQL or code.
#
# HOW TO ACCESS:
#   1. python manage.py createsuperuser  → creates an admin account
#   2. python manage.py runserver        → starts the server
#   3. Go to http://127.0.0.1:8000/admin/ in the browser
#   4. Log in with the superuser credentials
#   5. Click "Custom Users" to manage all registered user accounts
#
# WHAT THIS FILE DOES:
#   Without this file, CustomUser would NOT appear in the admin panel.
#   @admin.register(CustomUser) tells Django: "Show CustomUser in the admin, using CustomUserAdmin settings."
# ===================================================================================================================

from django.contrib import admin    # Django's built-in admin registration system
from .models import CustomUser      # Import CustomUser from users/models.py to register it with the admin site


@admin.register(CustomUser)         # Decorator that registers CustomUser with the admin site using this class as config
class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CustomUser model.
    ModelAdmin controls how user records are displayed and filtered in the admin panel.
    """

    # list_display: columns shown in the user list table view in the admin panel.
    # Each string is a field name from CustomUser. Django will render each as a sortable column header.
    # Example table row: | Sarah Martin | sarah@email.com | 25 | female | loss | moderate |
    list_display = ['name', 'email', 'age', 'gender', 'goal', 'activity_level']

    # list_filter: adds a sidebar filter panel on the right side of the admin list view.
    # Clicking 'male' or 'female' under 'gender' shows only users with that gender value.
    # Clicking 'loss' under 'goal' shows only weight-loss users.
    list_filter = ['gender', 'goal', 'activity_level']

    # search_fields: adds a search bar at the top of the admin list.
    # When the admin types a name or email, Django does a SQL ILIKE query on these two fields.
    # Example: searching "sarah" will find users whose name or email contains "sarah" (case-insensitive)
    search_fields = ['name', 'email']