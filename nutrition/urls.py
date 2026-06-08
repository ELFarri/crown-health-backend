# ===================================================================================================================
# FILE: nutrition/urls.py
# PURPOSE: URL ROUTING for the Nutrition app.
#          Maps URL paths to view functions defined in nutrition/views.py.
#          This file is included by calal_backend/urls.py under the prefix: /api/nutrition/
#
# FULL ENDPOINT PATHS (after prefix /api/nutrition/):
#   GET  /api/nutrition/meals/       → meals_list()      → returns today's meals (or by ?date=YYYY-MM-DD)
#   POST /api/nutrition/meals/add/   → add_meal()        → logs a new meal for the authenticated user
#   GET  /api/nutrition/stats/       → nutrition_stats() → returns aggregated macros grouped by day
#
# NOTE: All 3 endpoints require JWT authentication (IsAuthenticated).
#       Flutter must send: Authorization: Bearer <access_token>
# ===================================================================================================================

from django.urls import path  # path() creates a URL → view function mapping
from . import views           # Import view functions from nutrition/views.py (relative import)

urlpatterns = [

    # GET /api/nutrition/meals/
    # → calls views.meals_list()
    # Returns list of logged meals for today (or a specific date via ?date=YYYY-MM-DD query param)
    # No name set here (anonymous route) — the Flutter app uses the full URL string directly
    path('meals/', views.meals_list),

    # POST /api/nutrition/meals/add/
    # → calls views.add_meal()
    # Accepts a JSON body and creates a new Meal row in the nutrition_meal table
    path('meals/add/', views.add_meal),

    # GET /api/nutrition/stats/?period=weekly  OR  ?period=monthly
    # → calls views.nutrition_stats()
    # Returns per-day aggregated totals (calories, protein, carbs, fat) for the last 7 or 30 days
    path('stats/', views.nutrition_stats),
]