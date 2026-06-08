# ===================================================================================================================
# FILE: workouts/urls.py
# PURPOSE: URL ROUTING for the Workouts app.
#          Maps URL paths to view functions in workouts/views.py.
#          Included by calal_backend/urls.py under the prefix: /api/workouts/
#
# FULL ENDPOINT PATHS:
#   GET    /api/workouts/workouts/        → workouts_list()        → global exercise catalogue (no auth required)
#   GET    /api/workouts/history/         → user_workout_history() → user's personal workout logs (auth required)
#   POST   /api/workouts/history/         → user_workout_history() → logs a new workout session (auth required)
#   DELETE /api/workouts/history/clear/   → clear_workout_history() → deletes all user workout logs (auth required)
# ===================================================================================================================

from django.urls import path  # path() creates a URL → view function mapping
from . import views           # Import all view functions from workouts/views.py


urlpatterns = [

    # GET /api/workouts/workouts/
    # → calls views.workouts_list()
    # Returns the complete global workout catalogue (all Workout objects)
    # PUBLIC endpoint — no JWT token required (used by exercise browser to populate the list)
    path('workouts/', views.workouts_list),

    # GET /api/workouts/history/         → returns user's logged workout history
    # POST /api/workouts/history/        → logs a new workout session for the authenticated user
    # Both methods handled by the SAME view function (user_workout_history checks request.method internally)
    # PROTECTED — requires Authorization: Bearer <access_token>
    path('history/', views.user_workout_history),

    # DELETE /api/workouts/history/clear/
    # → calls views.clear_workout_history()
    # Permanently deletes ALL workout log entries for the authenticated user
    # PROTECTED — requires Authorization: Bearer <access_token>
    # NOTE: 'clear/' must come BEFORE any <id>/ patterns to avoid route conflicts
    path('history/clear/', views.clear_workout_history),
]