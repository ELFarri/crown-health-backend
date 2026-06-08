# ===================================================================================================================
# FILE: foods/views.py
# PURPOSE: API ENDPOINTS for the Food ingredient database search.
#          Provides 2 public endpoints:
#            1. food_list   → GET /api/foods/list/      → returns a sample of 10 food items
#            2. food_search → GET /api/foods/search/?q= → searches food by name (autocomplete)
#
# NOTE: These endpoints are currently DISABLED in calal_backend/urls.py (commented out).
#       To re-enable: uncomment path('api/foods/', include('foods.urls')) in calal_backend/urls.py
#
# USE CASE:
#   When a user types a food name in the meal logging screen, Flutter calls:
#   GET /api/foods/search/?q=chicken → returns matching food items with nutritional data
#   The user selects a result → nutritional values are auto-filled into the meal form
# ===================================================================================================================

from rest_framework.decorators import api_view  # DRF decorator to turn a function into an API view
from rest_framework.response import Response     # DRF JSON response wrapper
from .models import Food                         # Import the Food model (foods_food SQL table)
from .serializers import FoodSerializer          # Serializer to convert Food objects to JSON


# ===================================================================================================================
# ENDPOINT 1: GET /api/foods/list/
# PURPOSE: Returns the first 10 food items from the database (quick sample / health check).
# ACCESS: PUBLIC — no authentication required
# RESPONSE (HTTP 200 OK):
#   { "success": true, "count": 10,
#     "foods": [ { "id": 1, "name": "Grilled Chicken", "calories": 165, ... }, ... ] }
# ===================================================================================================================
@api_view(['GET'])  # Only accepts HTTP GET requests; no auth required
def food_list(request):
    # Fetch the first 10 food items from the foods_food table ([:10] = SQL LIMIT 10)
    # No ordering specified → returns in default ordering defined in Food.Meta (alphabetical by name)
    foods = Food.objects.all()[:10]

    # Serialize the QuerySet into a list of JSON-serializable dicts
    serializer = FoodSerializer(foods, many=True)

    # Return a structured response with metadata:
    # 'success' → indicates the request was processed successfully
    # 'count'   → number of food items returned (helps Flutter know list size without counting)
    # 'foods'   → the actual array of serialized food objects
    return Response({
        'success': True,
        'count': foods.count(),   # .count() runs a SQL COUNT query (more efficient than len())
        'foods': serializer.data  # List of food dicts (id, name, brand, category, calories, protein, etc.)
    })


# ===================================================================================================================
# ENDPOINT 2: GET /api/foods/search/?q=<query>
# PURPOSE: Searches the food database by name for autocomplete functionality in the meal logging screen.
# ACCESS: PUBLIC — no authentication required
# QUERY PARAM: ?q=<search_term>  (required — empty query returns nothing)
# EXAMPLE: GET /api/foods/search/?q=chicken → returns up to 5 foods whose name contains "chicken"
# RESPONSE (HTTP 200 OK):
#   [ { "id": 1, "name": "Grilled Chicken", "calories": 165, "protein": 31, ... },
#     { "id": 8, "name": "Chicken Breast", "calories": 120, "protein": 22, ... } ]
# ===================================================================================================================
@api_view(['GET'])
def food_search(request):
    # Extract the 'q' query parameter from the URL
    # Example: /api/foods/search/?q=banana → query = "banana"
    # Default to empty string '' if not provided
    query = request.GET.get('q', '')

    if query:
        # Case-insensitive name search: icontains → SQL LIKE '%banana%' (case-insensitive)
        # Limit to 5 results [:5] to keep the autocomplete dropdown small and fast
        foods = Food.objects.filter(name__icontains=query)[:5]
    else:
        # No search term provided → return empty QuerySet (no results, not an error)
        # Food.objects.none() → returns an empty QuerySet without hitting the database
        foods = Food.objects.none()

    # Serialize the results and return as a JSON array
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)