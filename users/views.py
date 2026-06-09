# ===================================================================================================================
# FILE: users/views.py
# PURPOSE: API ENDPOINTS for User Authentication and Profile Management.
#          This file contains 3 API endpoint functions (called "views" in Django):
#            1. register_api  → Creates a new user account (POST /api/users/register/)
#            2. login_api     → Authenticates a user and returns JWT tokens (POST /api/users/login/)
#            3. profile_api   → Fetches or updates the logged-in user's profile (GET/PUT/PATCH /api/users/profile/)
#
# AUTHENTICATION SYSTEM USED: JWT (JSON Web Token)
#   - On successful login, the server issues 2 tokens:
#       * ACCESS TOKEN  → short-lived (60 min), sent with every API request in the Authorization header
#       * REFRESH TOKEN → long-lived (1 day), used to get a new access token without re-logging in
#   - Flutter stores these tokens in SharedPreferences and attaches them as: "Authorization: Bearer <access_token>"
#
# HOW A PROTECTED REQUEST WORKS:
#   1. Flutter app adds the header: Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
#   2. Django's JWTAuthentication middleware reads the token and verifies its signature using SECRET_KEY
#   3. If valid, Django sets request.user = the CustomUser who owns the token
#   4. The view can then safely use request.user to access or modify that user's data
# ===================================================================================================================

# Django REST Framework decorators:
# @api_view(['POST']) → wraps a plain Python function into a DRF API view, restricts it to POST-only requests
# @permission_classes → applies access control rules (who can call this endpoint)
from rest_framework.decorators import api_view, permission_classes

# Permission classes:
# AllowAny → anyone (even unauthenticated users) can call this endpoint — needed for register and login
# IsAuthenticated → only users who sent a valid JWT token can access this endpoint
from rest_framework.permissions import AllowAny, IsAuthenticated

# Response → DRF's HTTP response wrapper that automatically serializes Python dicts to JSON
from rest_framework.response import Response

# RefreshToken → SimpleJWT's class for generating JWT access + refresh token pairs
from rest_framework_simplejwt.tokens import RefreshToken

# Import the CustomUser model to query the database
from .models import CustomUser

# Import the serializer that validates and converts CustomUser data to/from JSON
from .serializers import CustomUserSerializer


# ===================================================================================================================
# ENDPOINT 1: POST /api/users/register/
# PURPOSE: Creates a new user account in the database.
# ACCESS: Public — no authentication required (AllowAny)
# REQUEST BODY (JSON):
#   { "username": "sarah", "email": "sarah@email.com", "password": "secret123",
#     "name": "Sarah", "age": 25, "gender": "female", "height": 165, "weight": 60,
#     "goal": "loss", "activity_level": "moderate" }
# RESPONSE (success - HTTP 201 Created):
#   { "message": "User registered successfully!", "user_id": 5 }
# RESPONSE (error - HTTP 400 Bad Request):
#   { "username": ["A user with that username already exists."] }
# ===================================================================================================================
@api_view(['POST'])                   # This view only accepts POST requests. Any other method returns HTTP 405.
@permission_classes([AllowAny])       # No authentication required — anonymous users can register
def register_api(request):
    # Pass the incoming JSON request body (request.data) to the CustomUserSerializer for validation.
    # The serializer will check: required fields, email uniqueness, username uniqueness, password strength, etc.
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        # All validation passed → call serializer.save() which internally calls CustomUserSerializer.create()
        # create() calls User.objects.create_user() which hashes the password before saving to the database
        user = serializer.save()

        # Return HTTP 201 Created with a success message and the new user's database ID
        return Response({
            "message": "User registered successfully!",
            "user_id": user.id   # The auto-incremented primary key assigned by SQLite to the new row
        }, status=201)

    # Validation failed → return HTTP 400 Bad Request with field-level error messages
    # Example: {"email": ["This field must be unique."]}
    return Response(serializer.errors, status=400)


# ===================================================================================================================
# ENDPOINT 2: POST /api/users/login/
# PURPOSE: Authenticates a user by username/email + password, and returns JWT tokens.
# ACCESS: Public — no authentication required (AllowAny)
# REQUEST BODY (JSON):
#   { "username": "sarah@email.com", "password": "secret123" }
#   OR: { "email": "sarah@email.com", "password": "secret123" }
# RESPONSE (success - HTTP 200 OK):
#   { "access": "eyJ...", "refresh": "eyJ...", "user": { "id": 5, "username": "sarah", "email": "...", "name": "Sarah" } }
# RESPONSE (error - HTTP 401 Unauthorized):
#   { "error": "Invalid credentials" }
# ===================================================================================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    # Log the incoming request data to the Django console for debugging purposes
    print(f"Login attempt: {request.data}")

    # Extract 'username' from the request body. If not provided, fall back to 'email'.
    # This allows the Flutter app to send either field — both are accepted as the login identifier.
    username = request.data.get('username') or request.data.get('email')

    # Extract the plain-text password (it will be compared against the stored bcrypt hash)
    password = request.data.get('password')

    # Import Q (query object) to build complex OR database queries
    from django.db.models import Q

    # Search the database for a user whose username OR email matches the provided identifier.
    # Q(username=username) | Q(email=username) → SQL: WHERE username='...' OR email='...'
    # .first() → returns the first matching user object, or None if no match found
    user = CustomUser.objects.filter(Q(username=username) | Q(email=username)).first()

    if user and user.check_password(password):
        # check_password() compares the plain-text password against the stored bcrypt hash
        # If both the user exists AND the password is correct:

        # Generate a JWT token pair for this user:
        # refresh → the long-lived refresh token (valid 1 day, configured in settings.py SIMPLE_JWT)
        # refresh.access_token → the short-lived access token (valid 60 min)
        refresh = RefreshToken.for_user(user)

        # Return HTTP 200 OK with both tokens and basic user info
        # Flutter stores the 'access' token and sends it with every subsequent API request
        return Response({
            'access': str(refresh.access_token),   # Convert token object to JWT string (e.g. "eyJhbGci...")
            'refresh': str(refresh),               # Refresh token string for requesting new access tokens
            'user': {
                'id': user.id,                     # Database primary key
                'username': user.username,         # Login username
                'email': user.email,               # Email address
                'name': user.name                  # Display name
            }
        })

    # Authentication failed: either user not found OR password incorrect
    # Return HTTP 401 Unauthorized (do NOT reveal which part is wrong — security best practice)
    return Response({"error": "Invalid credentials"}, status=401)


# ===================================================================================================================
# ENDPOINT 3: GET/PUT/PATCH /api/users/profile/
# PURPOSE: Fetches the logged-in user's full profile (GET) or updates it (PUT/PATCH).
# ACCESS: Protected — requires a valid JWT access token in the Authorization header
# GET RESPONSE (HTTP 200 OK):
#   { "username": "sarah", "email": "...", "name": "Sarah", "age": 25, "gender": "female",
#     "height": 165.0, "weight": 60.0, "goal": "loss", "activity_level": "moderate" }
# PUT/PATCH REQUEST BODY (JSON): any subset of the fields above
# PUT/PATCH RESPONSE (HTTP 200 OK): the full updated user object
# ===================================================================================================================
@api_view(['GET', 'PUT', 'PATCH'])   # This view accepts GET (read) and PUT/PATCH (update) requests
@permission_classes([IsAuthenticated]) # JWT token REQUIRED — unauthenticated requests return HTTP 401
def profile_api(request):
    # request.user is automatically populated by Django's JWTAuthentication middleware.
    # It contains the full CustomUser object of the token's owner — no manual lookup needed.
    user = request.user

    if request.method in ['PUT', 'PATCH']:
        # partial=True → allows PATCH behavior: only update the fields that were sent.
        # Without partial=True, all required fields must be present (strict PUT replacement).
        # Example: PATCH with just {"weight": 65.0} → only updates weight, leaves everything else unchanged.
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Save the validated changes to the database (runs SQL UPDATE on the users_customuser table)
            serializer.save()
            # Return HTTP 200 OK with the complete updated user profile as JSON
            return Response(serializer.data)

        # Validation failed → return field-level error messages
        return Response(serializer.errors, status=400)

    # Default branch: GET request → serialize and return the current user's profile
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)   # Returns HTTP 200 OK with user data as JSON


# ===================================================================================================================
# ENDPOINT 4: GET /api/users/config/
# PURPOSE: Fetches configuration constants securely (such as the Gemini API Key) from the server environment.
# ACCESS: Protected — requires a valid JWT access token
# RESPONSE (success - HTTP 200 OK):
#   { "gemini_api_key": "..." }
# ===================================================================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def config_api(request):
    import os
    # Read the Gemini key from the environment variables (no hardcoded secrets in codebase)
    api_key = os.environ.get('GEMINI_API_KEY', '')
    return Response({
        "gemini_api_key": api_key
    })