# ===================================================================================================================
# FILE: users/models.py
# PURPOSE: Defines the CUSTOM USER MODEL — the central database table that stores every registered user's
#          profile, biometric data, and fitness goals in the Calal application.
#
# WHY A CUSTOM USER MODEL?
#   Django comes with a default User model that only stores: username, email, password, first_name, last_name.
#   For Calal, we need extra fields like: weight, height, age, gender, goal, activity_level.
#   By inheriting from AbstractUser, we EXTEND Django's default user system without rewriting the entire
#   authentication infrastructure (login, password hashing, permissions, admin panel support).
#
# DATABASE TABLE: This model maps to a single SQL table named "users_customuser" in db.sqlite3.
#   Each field below = one column in that table.
#
# RELATIONSHIP TO OTHER TABLES:
#   - nutrition/models.py → Meal has a ForeignKey(CustomUser) → each meal belongs to one user
#   - workouts/models.py  → UserWorkout has a ForeignKey(CustomUser) → each workout log belongs to one user
# ===================================================================================================================

from django.db import models                          # Django's ORM (Object Relational Mapper) — maps Python classes to SQL tables
from django.contrib.auth.models import AbstractUser   # Base class with full authentication logic (login, password, sessions)


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser with biometric and fitness-specific fields.
    AbstractUser already provides: username, email, password (hashed), is_active, date_joined, last_login, etc.
    We only define the EXTRA fields that the Calal app needs.
    """

    # --- EXTRA PROFILE FIELDS ---

    # Full display name of the user (e.g. "Sarah Martin"). Can be left blank during registration.
    # max_length=100 → SQL column type: VARCHAR(100)
    # blank=True → the field is optional in forms and the API (validation level)
    name = models.CharField(max_length=100, blank=True)

    # User's email address. Overrides AbstractUser's default email field to enforce uniqueness.
    # unique=True → the database creates a UNIQUE INDEX on this column, preventing duplicate accounts
    # This is used as the login identifier in login_api (alongside username)
    email = models.EmailField(unique=True)

    # User's age in years. Used in the BMR calculation formula on the frontend (Mifflin-St Jeor equation).
    # null=True  → the database column allows SQL NULL (no value stored)
    # blank=True → the field is optional during API requests
    age = models.IntegerField(null=True, blank=True)

    # --- DROPDOWN CHOICES (enforced at model + form validation level) ---

    # GENDER_CHOICES: list of tuples → (database_value, human_readable_label)
    # The first element ('male') is what gets stored in the database column.
    # The second element ('Male') is displayed in the Django admin panel dropdown.
    GENDER_CHOICES = [
        ('male', 'Male'),       # Stored as 'male' in DB
        ('female', 'Female'),   # Stored as 'female' in DB
    ]

    # GOAL_CHOICES: defines the user's primary fitness objective.
    # Used by the frontend to adjust the calorie target (TDEE - 500, TDEE, TDEE + 500)
    GOAL_CHOICES = [
        ('loss', 'Weight Loss'),       # User wants to lose weight → frontend applies a 500 kcal deficit
        ('gain', 'Weight Gain'),       # User wants to gain muscle → frontend adds 500 kcal surplus
        ('maintain', 'Maintain Weight'), # User wants to maintain → frontend uses TDEE directly
    ]

    # ACTIVITY_LEVEL_CHOICES: defines how physically active the user is in daily life.
    # Used to determine the PAL (Physical Activity Level) multiplier in the TDEE formula:
    #   TDEE = BMR × PAL multiplier
    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary'),           # Desk job, little or no exercise → multiplier: 1.2
        ('light', 'Light Exercise'),           # Light exercise 1-3 days/week → multiplier: 1.375
        ('moderate', 'Moderate Exercise'),     # Moderate exercise 3-5 days/week → multiplier: 1.55
        ('active', 'Active'),                  # Hard exercise 6-7 days/week → multiplier: 1.725
        ('very_active', 'Very Active'),        # Very hard exercise + physical job → multiplier: 1.9
    ]

    # --- BIOMETRIC FIELDS ---

    # Gender field: stores one of 'male' or 'female'.
    # max_length=10 → must be large enough to store the longest CHOICE value ('female' = 6 chars)
    # choices=GENDER_CHOICES → restricts valid values to the GENDER_CHOICES list (validated at form/serializer level)
    # blank=True → optional (user can fill this in during onboarding after registration)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    # Height in centimeters (e.g. 175.0 cm). Used in the Mifflin-St Jeor BMR formula.
    # FloatField → SQL REAL column (stores decimal numbers)
    # null=True / blank=True → optional field (filled during onboarding)
    height = models.FloatField(null=True, blank=True)

    # Current body weight in kilograms (e.g. 72.5 kg). Used in BMR calculation and BMI calculation.
    # FloatField → allows decimal precision (e.g. 72.5 instead of just 72)
    weight = models.FloatField(null=True, blank=True)

    # The user's primary fitness goal. Stored as 'loss', 'gain', or 'maintain' in the DB.
    # max_length=10 → must fit the longest value ('maintain' = 8 chars)
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES, blank=True)

    # The user's activity level key. Stored as e.g. 'moderate' in the DB.
    # max_length=20 → must fit the longest value ('very_active' = 11 chars) with room to spare
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, blank=True)

    def __str__(self):
        """
        String representation of the CustomUser object.
        Used by Django admin panel to display user records in list views.
        Returns the username (e.g. 'sarah_martin') instead of the default 'CustomUser object (1)'.
        """
        return self.username