# ===================================================================================================================
# FILE: users/urls.py
# PURPOSE: URL ROUTING for the Users app.
#          Maps URL paths to view functions defined in users/views.py.
#          This file is included by the root urls.py under the prefixes:
#            - /api/users/  → path('api/users/', include('users.urls'))
#            - /api/auth/   → path('api/auth/',  include('users.urls'))  [alias for flexibility]
#
# FULL ENDPOINT PATHS (after prefix):
#   POST /api/users/register/  → register_api()  → creates a new user account
#   POST /api/users/login/     → login_api()     → authenticates user, returns JWT tokens
#   GET  /api/users/profile/   → profile_api()   → returns the logged-in user's biometric profile
#   PUT  /api/users/profile/   → profile_api()   → fully replaces the user's profile data
#   PATCH /api/users/profile/  → profile_api()   → partially updates specific profile fields
# ===================================================================================================================

from django.urls import path  # path() creates a URL pattern: maps a string URL to a view function
from . import views           # Import all view functions from users/views.py (relative import using '.')

# urlpatterns: list of URL-to-view mappings for the users app.
# Django receives the URL suffix AFTER stripping the app prefix (e.g. 'register/' after stripping 'api/users/')
urlpatterns = [

    # POST /api/users/register/
    # Calls views.register_api — creates a new user account in the database
    # name='register' → allows reverse URL resolution: reverse('register') returns '/api/users/register/'
    path('register/', views.register_api, name='register'),

    # POST /api/users/login/
    # Calls views.login_api — verifies credentials and returns JWT access + refresh tokens
    # name='login' → used for reverse URL resolution in tests and other parts of the app
    path('login/', views.login_api, name='login'),

    # GET / PUT / PATCH /api/users/profile/
    # Calls views.profile_api — reads or updates the authenticated user's profile
    # Requires Authorization: Bearer <access_token> header (IsAuthenticated permission)
    # name='profile' → used for reverse URL resolution
    path('profile/', views.profile_api, name='profile'),
]