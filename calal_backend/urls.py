# ===================================================================================================================
# FILE: calal_backend/urls.py
# PURPOSE: ROOT URL ROUTER — the master URL configuration file for the entire Django project.
#          Every incoming HTTP request first arrives here. Django reads this file to decide which
#          app's urls.py should handle the request, based on the URL prefix.
#
# HOW URL ROUTING WORKS (step-by-step):
#   1. Flutter sends an HTTP request to e.g. POST /api/users/register/
#   2. Django receives the request and opens THIS file
#   3. Django scans urlpatterns top-to-bottom looking for a prefix match
#   4. It finds path('api/users/', ...) → strips 'api/users/' → passes 'register/' to users/urls.py
#   5. users/urls.py finds path('register/', ...) → calls views.register_api()
#   6. The view returns a JSON Response back to Flutter
#
# REGISTERED API ENDPOINTS (full paths):
#   POST   /api/users/register/          → User registration
#   POST   /api/users/login/             → User login (returns JWT tokens)
#   GET    /api/users/profile/           → Fetch user profile
#   PUT    /api/users/profile/           → Update user profile
#   POST   /api/auth/register/           → Same as above (duplicate route for flexibility)
#   POST   /api/auth/login/              → Same as above (duplicate route for flexibility)
#   GET    /api/nutrition/meals/         → List today's meals
#   POST   /api/nutrition/meals/add/     → Add a new meal
#   GET    /api/nutrition/stats/         → Aggregated nutrition statistics (weekly/monthly)
#   GET    /api/workouts/workouts/       → List all available workouts from the catalogue
#   GET    /api/workouts/history/        → Get user's personal workout history
#   POST   /api/workouts/history/        → Log a new workout session
#   DELETE /api/workouts/history/clear/  → Delete all user workout history
#   GET    /admin/                       → Django admin panel (browser-based database management UI)
# ===================================================================================================================

from django.contrib import admin          # Import Django's built-in admin module to register the /admin/ panel route
from django.urls import path, include     # path() → creates a URL pattern; include() → delegates to another urls.py file
from django.conf import settings          # Import settings to access DEBUG, MEDIA_URL, MEDIA_ROOT variables
from django.conf.urls.static import static # Helper to serve uploaded media files (e.g. images) during development

# urlpatterns: the ordered list of URL patterns that Django will try to match against incoming HTTP requests.
# Django scans this list from top to bottom and stops at the FIRST match.
urlpatterns = [

    # Route: /admin/
    # Mounts Django's built-in admin panel at /admin/
    # The admin panel gives a full browser-based CRUD interface for all registered models (CustomUser, Meal, Workout, etc.)
    # Access: http://127.0.0.1:8000/admin/ (requires a superuser account created with: python manage.py createsuperuser)
    path('admin/', admin.site.urls),

    # Route: /api/users/
    # Delegates all requests starting with 'api/users/' to the users app's urls.py
    # include('users.urls') → imports and appends the urlpatterns list from users/urls.py
    # Resulting endpoints: /api/users/register/, /api/users/login/, /api/users/profile/
    path('api/users/', include('users.urls')),

    # Route: /api/auth/
    # An ALIAS pointing to the same users/urls.py (same views, different URL prefix)
    # This allows the Flutter app to call either /api/users/login/ OR /api/auth/login/ — both work
    # Useful for frontend flexibility and matches common REST API conventions
    path('api/auth/', include('users.urls')),

    # Route: /api/nutrition/
    # Delegates all requests starting with 'api/nutrition/' to nutrition/urls.py
    # Resulting endpoints: /api/nutrition/meals/, /api/nutrition/meals/add/, /api/nutrition/stats/
    path('api/nutrition/', include('nutrition.urls')),

    # Route: /api/workouts/
    # Delegates all requests starting with 'api/workouts/' to workouts/urls.py
    # Resulting endpoints: /api/workouts/workouts/, /api/workouts/history/, /api/workouts/history/clear/
    path('api/workouts/', include('workouts.urls')),

    # NOTE: Foods API is currently DISABLED (commented out)
    # Uncomment the line below to re-enable the food search and list endpoints:
    # path('api/foods/', include('foods.urls')),
]

# MEDIA FILE SERVING (Development only):
# During local development (when DEBUG=True in settings.py), Django does not serve media files by default.
# This line adds a special URL pattern that maps requests to MEDIA_URL (/media/) to files stored in MEDIA_ROOT.
# Example: A request to /media/profile_pictures/photo.jpg is served from the filesystem at BASE_DIR/media/
# WARNING: This should NEVER be used in production. In production, a web server like Nginx handles static files.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)