# ===================================================================================================================
# FILE: workouts/models.py
# PURPOSE: Defines TWO database models for workout tracking:
#
#   1. Workout       → The GLOBAL CATALOGUE of available workouts (shared across all users)
#                      Table: workouts_workout
#                      Examples: "Bench Press", "Running", "Squats"
#
#   2. UserWorkout   → A PERSONAL LOG entry: records that a specific user performed a specific workout
#                      Table: workouts_userworkout
#                      Examples: "User #5 did Bench Press for 45 minutes on 2024-06-07"
#
# RELATIONSHIP DIAGRAM:
#   CustomUser ──< UserWorkout >── Workout
#   (one user has many workout logs, each log references one workout from the catalogue)
#
# WHY TWO SEPARATE TABLES?
#   - Workout (catalogue) stores the BASE data: standard name, category, and reference calorie burn per standard duration
#   - UserWorkout (log) stores VARIABLE data: actual duration performed, date, which user did it
#   - This allows dynamic calorie calculation: if the base workout burns 300 kcal in 60 min,
#     and the user did it for 30 min → burned = 300 × (30/60) = 150 kcal
#     (computed in workouts/serializers.py via to_representation())
# ===================================================================================================================

from django.db import models        # Django ORM: maps Python classes to SQL tables
from users.models import CustomUser # Import CustomUser to create the ForeignKey relationship


class Workout(models.Model):
    """
    Global workout catalogue entry. Not linked to any specific user.
    Defines the base properties of a type of exercise.
    One Workout can be referenced by MANY UserWorkout log entries.
    """

    # Name of the exercise (e.g. "Bench Press", "Running", "Yoga").
    # max_length=100 → VARCHAR(100) in SQL
    name = models.CharField(max_length=100)

    # Muscle group or exercise category (e.g. "Chest", "Cardio", "Legs", "Back").
    # max_length=50 → VARCHAR(50) in SQL
    # Used by the Flutter app to group and filter exercises by body part
    category = models.CharField(max_length=50)

    # The REFERENCE duration of this workout in minutes.
    # Used as the denominator in the calorie ratio calculation.
    # Example: if duration_minutes=60, and the user worked out for 30 min,
    # the calorie burn ratio = 30/60 = 0.5
    duration_minutes = models.IntegerField()  # IntegerField → SQL INTEGER column (whole numbers)

    # The BASE calorie burn for this workout at its reference duration.
    # Stored in kcal (kilocalories). Example: Running for 60 min burns 500 kcal.
    # Actual kcal = calories_burned × (user_duration / duration_minutes)
    calories_burned = models.IntegerField()

    def __str__(self):
        """Admin panel display: shows the workout name (e.g. "Bench Press")"""
        return self.name


class UserWorkout(models.Model):
    """
    Personal workout log entry. Records that a specific user performed a specific workout.
    One row = one workout session logged by one user on one date.
    """

    # FOREIGN KEY → links this log to the user who performed the workout.
    # on_delete=models.CASCADE → if the user is deleted, all their workout logs are deleted too.
    # SQL: user_id INTEGER NOT NULL REFERENCES users_customuser(id) ON DELETE CASCADE
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # FOREIGN KEY → links this log to a specific workout from the global catalogue.
    # on_delete=models.CASCADE → if a Workout is deleted from the catalogue, all related logs are deleted.
    # SQL: workout_id INTEGER NOT NULL REFERENCES workouts_workout(id) ON DELETE CASCADE
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)

    # The date this workout session was performed.
    # auto_now_add=True → automatically set to TODAY when the log row is first created (server-side).
    # DateField → SQL DATE column (stores "2024-06-07", no time component)
    date = models.DateField(auto_now_add=True)

    # The ACTUAL duration the user performed this workout in minutes.
    # This may differ from Workout.duration_minutes (the reference duration).
    # Example: base workout is 60 min, user only did 45 min → duration=45
    # Used by the serializer to compute the proportional calorie burn.
    duration = models.IntegerField()