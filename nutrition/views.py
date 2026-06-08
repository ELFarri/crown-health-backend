# ===================================================================================================================
# FILE: nutrition/views.py
# PURPOSE: API ENDPOINTS for Meal Logging and Nutrition Statistics.
#          Contains 3 endpoint functions:
#            1. meals_list      → GET  /api/nutrition/meals/        → Returns today's (or any date's) meals
#            2. add_meal        → POST /api/nutrition/meals/add/    → Saves a new meal to the database
#            3. nutrition_stats → GET  /api/nutrition/stats/        → Returns aggregated weekly/monthly stats
#
# ALL ENDPOINTS REQUIRE AUTHENTICATION (IsAuthenticated):
#   Flutter must send: Authorization: Bearer <access_token> in every request header.
#   Django's JWTAuthentication middleware verifies the token and sets request.user automatically.
#   This ensures each user can ONLY see and modify their OWN meal data (data isolation).
#
# DATA FLOW EXAMPLE (logging a meal):
#   Flutter user taps "Add Meal" → sends POST /api/nutrition/meals/add/ with JSON body
#   → add_meal() receives request.data → MealSerializer validates fields
#   → serializer.save(user=request.user) → INSERT INTO nutrition_meal (user_id, name, calories, ...) VALUES (...)
#   → Django returns HTTP 201 Created with the saved meal as JSON
#   → Flutter updates the UI with the new meal in the diary
# ===================================================================================================================

from rest_framework.decorators import api_view, permission_classes  # DRF decorators to define API views
from rest_framework.permissions import IsAuthenticated               # Permission: only authenticated users allowed
from rest_framework.response import Response                         # DRF JSON response wrapper
from .models import Meal                                             # Meal model (nutrition_meal SQL table)
from .serializers import MealSerializer                              # Serializer for Meal model validation & conversion
from users.models import CustomUser                                  # CustomUser model (imported but not directly used here)
from django.utils import timezone                                     # Django's timezone-aware datetime utilities
import datetime                                                       # Python's standard datetime module for date parsing

# ===================================================================================================================
# ENDPOINT 1: GET /api/nutrition/meals/
# PURPOSE: Returns the list of meals logged by the authenticated user for a specific date.
#          Defaults to TODAY if no date is provided.
# QUERY PARAM: ?date=YYYY-MM-DD  (optional) → filter meals for that specific date
# EXAMPLE CALLS:
#   GET /api/nutrition/meals/                  → returns today's meals
#   GET /api/nutrition/meals/?date=2024-06-01  → returns meals logged on June 1st
# RESPONSE (HTTP 200 OK):
#   [ { "id": 1, "name": "Chicken", "calories": 165, "protein": 31.0, "carbs": 0.0, "fat": 3.6,
#       "meal_type": "lunch", "date": "2024-06-07", "user": 5 }, ... ]
# ===================================================================================================================
@api_view(['GET'])                     # Only accepts HTTP GET requests
@permission_classes([IsAuthenticated]) # JWT token required — anonymous requests return HTTP 401
def meals_list(request):
    # Read the optional 'date' query parameter from the URL
    # Example: /api/nutrition/meals/?date=2024-06-01 → date_param = "2024-06-01"
    # If not provided → date_param = None
    date_param = request.GET.get('date', None)

    if date_param:
        try:
            # Parse the date string into a Python date object using ISO 8601 format (YYYY-MM-DD)
            # datetime.date.fromisoformat("2024-06-07") → datetime.date(2024, 6, 7)
            target_date = datetime.date.fromisoformat(date_param)
        except ValueError:
            # If the date string is malformed (e.g. "06/07/2024"), return HTTP 400 Bad Request
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
    else:
        # No date provided → default to today's date using Django's timezone-aware now()
        # timezone.now().date() → returns today's date in the server's configured timezone
        target_date = timezone.now().date()

    # Query the database: SELECT * FROM nutrition_meal WHERE user_id=<request.user.id> AND date=<target_date>
    # This ensures users can ONLY see their OWN meals — never another user's data
    meals = Meal.objects.filter(user=request.user, date=target_date)

    # Serialize the QuerySet (list of Meal objects) into a JSON-serializable list of dicts
    # many=True → tells the serializer to handle a list of objects (not just one)
    serializer = MealSerializer(meals, many=True)

    # Return HTTP 200 OK with the serialized meal list as JSON
    return Response(serializer.data)


# ===================================================================================================================
# ENDPOINT 2: POST /api/nutrition/meals/add/
# PURPOSE: Adds a new meal entry to the database for the authenticated user.
# REQUEST BODY (JSON):
#   { "name": "Grilled Chicken", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "meal_type": "lunch" }
# RESPONSE (success - HTTP 201 Created):
#   { "id": 42, "name": "Grilled Chicken", "calories": 165, "protein": 31.0, "carbs": 0.0,
#     "fat": 3.6, "meal_type": "lunch", "date": "2024-06-07", "user": 5 }
# RESPONSE (error - HTTP 400 Bad Request):
#   { "calories": ["This field is required."] }
# ===================================================================================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_meal(request):
    # Initialize the serializer with the incoming JSON request body for validation
    # request.data → DRF automatically parses the JSON body into a Python dict
    serializer = MealSerializer(data=request.data)

    if serializer.is_valid():
        # user=request.user → injects the authenticated user as the meal owner BEFORE saving.
        # This is critical: the 'user' field is read_only in the serializer,
        # so it CANNOT be set by the client — only the server assigns it.
        # SQL: INSERT INTO nutrition_meal (user_id, name, calories, ...) VALUES (<token_user_id>, ...)
        serializer.save(user=request.user)

        # Return HTTP 201 Created with the full saved meal object (including auto-assigned id and date)
        return Response(serializer.data, status=201)

    # Validation failed → return HTTP 400 with field-level error messages
    return Response(serializer.errors, status=400)


# --- Additional imports needed for nutrition_stats (imported here to avoid circular import at top of file) ---
from django.db.models import Sum       # SQL aggregate function: SUM(calories), SUM(protein), etc.
from datetime import timedelta         # Python timedelta: used to calculate date ranges (today - 7 days)
from django.utils import timezone      # Re-imported (already above, kept for clarity)

# ===================================================================================================================
# ENDPOINT 3: GET /api/nutrition/stats/
# PURPOSE: Returns aggregated nutrition data (calories, protein, carbs, fat) grouped by date.
#          Powers the statistics charts in the Flutter Stats screen.
# QUERY PARAM: ?period=weekly (default) OR ?period=monthly
# EXAMPLE CALLS:
#   GET /api/nutrition/stats/              → last 7 days of nutrition data
#   GET /api/nutrition/stats/?period=monthly → last 30 days
# RESPONSE (HTTP 200 OK):
#   [ { "date": "2024-06-07", "total_calories": 1850, "total_protein": 120.5,
#       "total_carbs": 200.0, "total_fat": 65.2 }, ... ]
# ===================================================================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nutrition_stats(request):
    # Read the 'period' query param from the URL. Default is 'weekly' if not provided.
    period = request.GET.get('period', 'weekly')

    # Get today's date using the server's timezone
    today = timezone.now().date()

    if period == 'monthly':
        # Monthly view: go back 30 days from today
        start_date = today - timedelta(days=30)
    else:
        # Weekly view (default): go back 7 days from today
        start_date = today - timedelta(days=7)

    # Complex ORM query that performs SQL GROUP BY + aggregate SUM operations:
    # 1. .filter() → WHERE user_id=<token_user> AND date >= <start_date>
    # 2. .values('date') → GROUP BY date (one result row per day)
    # 3. .annotate() → adds aggregate columns: SUM(calories) AS total_calories, etc.
    # 4. .order_by('-date') → ORDER BY date DESC (most recent day first)
    #
    # Equivalent SQL:
    # SELECT date,
    #        SUM(calories) AS total_calories,
    #        SUM(protein)  AS total_protein,
    #        SUM(carbs)    AS total_carbs,
    #        SUM(fat)      AS total_fat
    # FROM nutrition_meal
    # WHERE user_id = <request.user.id> AND date >= <start_date>
    # GROUP BY date
    # ORDER BY date DESC
    stats = Meal.objects.filter(
        user=request.user,    # Only this user's meals
        date__gte=start_date  # date >= start_date (gte = "greater than or equal")
    ).values('date').annotate(
        total_calories=Sum('calories'),  # SUM all calorie values per day
        total_protein=Sum('protein'),    # SUM all protein values per day
        total_carbs=Sum('carbs'),        # SUM all carbs values per day
        total_fat=Sum('fat')             # SUM all fat values per day
    ).order_by('-date')  # Most recent date first

    # list(stats) converts the Django QuerySet to a Python list of dicts for JSON serialization
    return Response(list(stats))