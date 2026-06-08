# ===================================================================================================================
# FILE: users/serializers.py
# PURPOSE: DATA VALIDATION & CONVERSION LAYER between JSON (HTTP) and Python objects (Django ORM).
#          A serializer acts as a two-way translator:
#            INCOMING (Deserialization): JSON request body → validated Python dict → database record
#            OUTGOING (Serialization):  database record → Python dict → JSON response
#
# WHY IS THIS NEEDED?
#   Django models work with Python objects. HTTP requests send raw JSON strings.
#   The serializer handles all the messy middle work:
#     - Parsing raw JSON fields
#     - Validating each field (correct type? required? unique?)
#     - Hashing the password BEFORE saving to database (critical for security)
#     - Converting Python objects back to JSON-serializable dictionaries
#
# EXAMPLE FLOW (Registration):
#   Flutter sends: POST /api/users/register/ with body {"username":"sarah","email":"...","password":"secret123",...}
#   → views.register_api receives request.data (a Python dict)
#   → CustomUserSerializer(data=request.data) initializes the serializer with that dict
#   → serializer.is_valid() validates all fields (email unique? password present?)
#   → serializer.save() calls CustomUserSerializer.create() → User.objects.create_user() → password hashed + saved
# ===================================================================================================================

from rest_framework import serializers         # DRF serializer base classes and field types
from django.contrib.auth import get_user_model  # Dynamic getter that returns the model set in AUTH_USER_MODEL (our CustomUser)
from .models import CustomUser                 # Direct import of our CustomUser model for type reference

# get_user_model() returns the CustomUser class (as defined in settings.py: AUTH_USER_MODEL = 'users.CustomUser')
# Using get_user_model() instead of importing CustomUser directly is the Django best practice —
# it avoids circular import issues in larger projects
User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Handles both READING (GET profile) and WRITING (POST register, PATCH update profile) operations.
    ModelSerializer automatically generates fields and validation rules based on the model definition.
    """

    # Override the default password field behavior:
    # By default, ModelSerializer would include password in both input AND output (GET responses).
    # write_only=True → the password is accepted in POST/PUT requests but NEVER included in GET responses.
    # This is a critical security rule: never expose hashed passwords in API responses.
    password = serializers.CharField(write_only=True)

    class Meta:
        """
        Meta class tells ModelSerializer which model to use and which fields to expose in the API.
        """
        model = User  # Link this serializer to the CustomUser database model

        # Explicit list of fields that will appear in API requests and responses.
        # These map directly to columns in the "users_customuser" database table.
        # 'password' is write_only (hidden in GET), all others are readable and writable.
        fields = [
            'username',        # Unique login handle (inherited from AbstractUser)
            'email',           # Unique email address (overridden to enforce uniqueness)
            'password',        # Plain-text password on input → gets hashed before saving (write_only)
            'name',            # Full display name
            'age',             # Age in years (used in BMR formula on the frontend)
            'gender',          # 'male' or 'female' (controls BMR formula coefficient)
            'height',          # Height in cm (used in BMR: 6.25 × height)
            'weight',          # Weight in kg (used in BMR: 10 × weight)
            'goal',            # 'loss', 'gain', or 'maintain' (controls calorie target offset)
            'activity_level',  # 'sedentary', 'light', 'moderate', 'active', 'very_active' (PAL multiplier)
        ]

    def create(self, validated_data):
        """
        Called automatically when serializer.save() is invoked on a NEW user (registration).
        validated_data → Python dict with all cleaned, validated field values from the request.

        IMPORTANT: We use create_user() instead of create() because:
          - create_user() automatically hashes the plain-text password using Django's bcrypt/PBKDF2 hasher
          - create() saves the password as plain text (a major security vulnerability)
          - **validated_data → unpacks the dict as keyword arguments: username=..., email=..., password=...
        """
        return User.objects.create_user(**validated_data)