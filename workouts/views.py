# ===================================================================================================================
# FILE: workouts/views.py
# PURPOSE: API ENDPOINTS for Workout Catalogue and Personal Workout History.
#          Contains 3 endpoint functions:
#            1. workouts_list         → GET    /api/workouts/workouts/    → Returns global workout catalogue (no auth)
#            2. user_workout_history  → GET    /api/workouts/history/     → Returns user's personal workout logs
#                                     → POST   /api/workouts/history/     → Logs a new workout session
#            3. clear_workout_history → DELETE /api/workouts/history/clear/ → Deletes ALL user workout history
#
# KEY DESIGN FEATURE — Smart Workout Creation (get_or_create):
#   When the Flutter app logs a custom workout (e.g. from the exercise browser), it sends the workout NAME
#   instead of a database ID. The view automatically finds or creates the Workout catalogue entry
#   before logging the UserWorkout. This prevents duplicate catalogue entries and keeps data clean.
#
# CALORIE CALCULATION:
#   Calories are NOT stored directly in UserWorkout. They are computed dynamically in the serializer:
#   actual_calories = base_calories × (user_duration / base_duration_minutes)
#   Example: Running base = 500 kcal/60min. User ran 30min → 500 × (30/60) = 250 kcal
# ===================================================================================================================

from rest_framework.decorators import api_view, permission_classes  # DRF view decorators
from rest_framework.permissions import IsAuthenticated               # JWT auth permission class
from rest_framework.response import Response                         # DRF JSON response
from .models import Workout, UserWorkout                             # Both workout models
from .serializers import WorkoutSerializer, UserWorkoutSerializer    # Both serializers
import datetime                                                       # For parsing date strings from query params


# ===================================================================================================================
# ENDPOINT 1: GET /api/workouts/workouts/
# PURPOSE: Returns the full list of workouts from the global Workout catalogue.
# ACCESS: PUBLIC — no authentication required (no @permission_classes decorator = AllowAny by default)
# USE CASE: Flutter's Exercise Browser screen fetches this list to let users pick an exercise to log.
# RESPONSE (HTTP 200 OK):
#   [ { "id": 1, "name": "Bench Press", "category": "Chest", "duration_minutes": 60, "calories_burned": 300 },
#     { "id": 2, "name": "Running", "category": "Cardio", "duration_minutes": 60, "calories_burned": 500 }, ... ]
# ===================================================================================================================
@api_view(['GET'])  # Only accepts HTTP GET — no auth required (public catalogue)
def workouts_list(request):
    # Fetch ALL rows from the workouts_workout table — no filtering needed (global catalogue)
    workouts = Workout.objects.all()

    # Serialize the full QuerySet into a list of JSON-serializable dicts
    # many=True → required when serializing a list of objects (not a single instance)
    serializer = WorkoutSerializer(workouts, many=True)

    # Return HTTP 200 OK with the full catalogue as a JSON array
    return Response(serializer.data)


# ===================================================================================================================
# ENDPOINT 2: GET + POST /api/workouts/history/
# PURPOSE (GET):  Returns the authenticated user's personal workout log history.
# PURPOSE (POST): Logs a new workout session for the authenticated user.
# ACCESS: PROTECTED — requires valid JWT token
#
# GET QUERY PARAM: ?date=YYYY-MM-DD (optional) → filter logs for that specific date only
# GET RESPONSE (HTTP 200 OK):
#   [ { "id": 5, "workout": 1, "workout_name": "Bench Press", "category": "Chest",
#       "date": "2024-06-07", "duration": 45, "calories_burned": 225 }, ... ]
#
# POST REQUEST BODY option A (with existing workout ID):
#   { "workout": 1, "duration": 45 }
# POST REQUEST BODY option B (with workout name — auto-creates catalogue entry if needed):
#   { "workout_name": "Pull-ups", "category": "Back", "duration": 30 }
# POST RESPONSE (HTTP 201 Created): the serialized UserWorkout object
# ===================================================================================================================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # JWT token required — request.user is auto-populated
def user_workout_history(request):

    if request.method == 'GET':
        # Read optional date filter from query parameters
        # Example: /api/workouts/history/?date=2024-06-07 → date_param = "2024-06-07"
        date_param = request.GET.get('date', None)

        # Start with all UserWorkout rows belonging to the authenticated user
        # SQL: SELECT * FROM workouts_userworkout WHERE user_id = <request.user.id>
        qs = UserWorkout.objects.filter(user=request.user)

        if date_param:
            try:
                # Parse the ISO date string into a Python date object
                target_date = datetime.date.fromisoformat(date_param)
                # Apply additional date filter: WHERE date = <target_date>
                qs = qs.filter(date=target_date)
            except ValueError:
                # Malformed date string → return HTTP 400
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        # Order results by date descending (most recent workout session first)
        history = qs.order_by('-date')

        # Serialize the filtered QuerySet into JSON
        serializer = UserWorkoutSerializer(history, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Make a mutable copy of the request data dict (request.data is immutable by default in DRF)
        data = request.data.copy()

        # Check if the Flutter app sent a workout catalogue ID directly
        workout_id = data.get('workout')

        if not workout_id:
            # No workout ID provided → Flutter sent a workout NAME instead (custom exercise flow)
            # Extract workout metadata from the request body with safe defaults
            workout_name = data.get('workout_name', 'Workout')  # Default name if not provided
            category = data.get('category', 'General')           # Default category
            duration = data.get('duration', 30)                  # Default duration in minutes

            # get_or_create(): atomically checks if a Workout with this name+category exists.
            # If YES → returns the existing object (avoids duplicates in the catalogue)
            # If NO  → creates a new Workout with the provided defaults and returns it
            # The '_' variable captures the boolean 'created' flag (True if new, False if existing)
            workout, _ = Workout.objects.get_or_create(
                name=workout_name,     # Lookup key: match by name
                category=category,     # Lookup key: match by category
                defaults={             # Values used ONLY when creating a new record (not for lookup)
                    'duration_minutes': duration,
                    'calories_burned': 250  # Default base calorie value for custom workouts
                }
            )
            # Inject the resolved or newly created workout ID into the data dict
            data['workout'] = workout.id

        # Validate and save the UserWorkout log entry
        serializer = UserWorkoutSerializer(data=data)
        if serializer.is_valid():
            # Inject the authenticated user as the owner before saving to the database
            # SQL: INSERT INTO workouts_userworkout (user_id, workout_id, duration, date) VALUES (...)
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)  # HTTP 201 Created

        # Validation failed → return error details
        return Response(serializer.errors, status=400)


# ===================================================================================================================
# ENDPOINT 3: DELETE /api/workouts/history/clear/
# PURPOSE: Permanently deletes ALL workout log entries for the authenticated user.
# ACCESS: PROTECTED — requires valid JWT token
# USE CASE: "Clear History" button in the Flutter workout history screen.
# RESPONSE (HTTP 200 OK): { "message": "Workout history cleared successfully!" }
# WARNING: This is a DESTRUCTIVE operation — deleted rows CANNOT be recovered.
# ===================================================================================================================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_workout_history(request):
    # Delete ALL UserWorkout rows where user_id matches the authenticated user
    # SQL: DELETE FROM workouts_userworkout WHERE user_id = <request.user.id>
    UserWorkout.objects.filter(user=request.user).delete()

    # Return HTTP 200 OK with a success confirmation message
    return Response({"message": "Workout history cleared successfully!"}, status=200)