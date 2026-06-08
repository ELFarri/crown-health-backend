# ===================================================================================================================
# FILE: nutrition/models.py
# PURPOSE: Defines the MEAL database model — the core table for tracking daily food intake per user.
#          Every time a user logs a meal in the Flutter app, one row is created in this table.
#
# DATABASE TABLE: "nutrition_meal" in db.sqlite3
#   Each row = one logged food item for one user on one specific date.
#
# RELATIONSHIP:
#   Meal → CustomUser via ForeignKey (MANY-TO-ONE):
#     - One user can have MANY meals
#     - Each meal belongs to exactly ONE user
#   SQL equivalent: FOREIGN KEY (user_id) REFERENCES users_customuser(id)
#
# EXAMPLE ROW IN DATABASE:
#   id=1, user_id=5, name="Grilled Chicken", calories=165, protein=31.0,
#   carbs=0.0, fat=3.6, meal_type="lunch", date="2024-06-07"
#
# HOW IT CONNECTS TO THE FLUTTER APP:
#   1. User opens the Meals screen → Flutter calls GET /api/nutrition/meals/?date=2024-06-07
#   2. Django queries: Meal.objects.filter(user=request.user, date=today)
#   3. Django serializes results → returns JSON array of meal rows
#   4. Flutter displays them in the diary with macronutrient breakdown
# ===================================================================================================================

from django.db import models        # Django ORM: maps Python classes to SQL tables
from users.models import CustomUser # Import CustomUser model to create the ForeignKey relationship


class Meal(models.Model):
    """
    Represents a single food item logged by a user on a specific date.
    Each instance = one row in the nutrition_meal SQL table.
    """

    # Predefined meal type categories. Stored as short string keys in the DB.
    # This list restricts valid values at the application level (not enforced by SQLite itself).
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),  # Morning meal (value stored in DB: 'breakfast')
        ('lunch', 'Lunch'),          # Midday meal (value stored in DB: 'lunch')
        ('dinner', 'Dinner'),        # Evening meal (value stored in DB: 'dinner')
        ('snack', 'Snack'),          # Between-meal snack (value stored in DB: 'snack')
    ]

    # FOREIGN KEY: links this meal to the user who logged it.
    # on_delete=models.CASCADE → if the user account is deleted, ALL their meals are automatically deleted too.
    # This prevents "orphan" meal rows in the database with no associated user.
    # In SQL: user_id INTEGER NOT NULL REFERENCES users_customuser(id) ON DELETE CASCADE
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Name of the food item (e.g. "Grilled Chicken", "Banana", "Protein Shake").
    # max_length=100 → VARCHAR(100) in SQL — limits to 100 characters
    name = models.CharField(max_length=100)

    # Total caloric value of the food item in kilocalories (kcal).
    # IntegerField → SQL INTEGER (whole numbers only, no decimals)
    # Used by the frontend to display the daily calorie total and progress bar.
    calories = models.IntegerField()

    # Protein content in grams. Used for macronutrient tracking.
    # FloatField → SQL REAL (allows decimal precision, e.g. 31.5g)
    # default=0 → if not provided by the client, the database stores 0.0
    protein = models.FloatField(default=0)

    # Carbohydrate content in grams. Used for macronutrient tracking and energy source analysis.
    carbs = models.FloatField(default=0)

    # Fat content in grams. Used for macronutrient tracking.
    fat = models.FloatField(default=0)

    # The meal category (breakfast, lunch, dinner, or snack).
    # max_length=50 → stores the MEAL_TYPES key value (e.g. 'breakfast')
    # NOTE: choices=MEAL_TYPES is NOT used here (field accepts any string), which gives more flexibility
    meal_type = models.CharField(max_length=50)

    # The date this meal was consumed.
    # auto_now_add=True → automatically sets this field to TODAY's date when the row is first created.
    # The user CANNOT override this value via the API — it is set server-side at creation time.
    # DateField → SQL DATE column (stores only the date, not the time: e.g. "2024-06-07")
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        Human-readable representation for the Django admin panel.
        Returns a formatted string like: "sarah_martin - Grilled Chicken"
        This makes it easy to identify meal records in admin list views.
        """
        return f"{self.user.username} - {self.name}"