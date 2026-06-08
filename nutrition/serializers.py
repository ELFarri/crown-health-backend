# ===================================================================================================================
# FILE: nutrition/serializers.py
# PURPOSE: Converts Meal model instances to/from JSON for the nutrition API endpoints.
#
# ROLE IN THE REQUEST PIPELINE:
#   INCOMING (POST /api/nutrition/meals/add/):
#     JSON body → MealSerializer(data=request.data) → .is_valid() validates fields → .save() creates DB row
#   OUTGOING (GET /api/nutrition/meals/):
#     Meal QuerySet → MealSerializer(meals, many=True) → .data → JSON array returned to Flutter
#
# KEY DESIGN DECISION — read_only_fields = ['user']:
#   The 'user' field is marked as READ-ONLY. This means:
#   - When the client sends a POST request, they CANNOT set the 'user' field in the JSON body.
#   - The 'user' is always injected server-side via: serializer.save(user=request.user)
#   - This is a critical SECURITY measure: prevents a malicious user from logging meals
#     under another user's account by sending a different user_id in the request body.
# ===================================================================================================================

from rest_framework import serializers  # DRF base serializer classes
from .models import Meal                # Import the Meal model to base this serializer on


class MealSerializer(serializers.ModelSerializer):
    """
    Serializer for the Meal model.
    Automatically generates fields for all model columns using fields = '__all__'.
    Controls which fields are readable/writable through read_only_fields.
    """

    class Meta:
        """Inner Meta class that configures which model and fields this serializer handles."""

        model = Meal          # Links this serializer to the Meal database model

        fields = '__all__'    # Expose ALL model fields in the API:
                              # id, user, name, calories, protein, carbs, fat, meal_type, date
                              # '__all__' is a shortcut — equivalent to listing every field explicitly

        read_only_fields = ['user']  # 'user' is OUTPUT-ONLY:
                                     # - Included in GET responses so Flutter knows which user owns the meal
                                     # - IGNORED in POST/PATCH request bodies (cannot be set by the client)
                                     # - Always set server-side in the view: serializer.save(user=request.user)
                                     # This prevents IDOR (Insecure Direct Object Reference) attacks