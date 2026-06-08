# ===================================================================================================================
# FILE: workouts/serializers.py
# PURPOSE: Converts Workout and UserWorkout model instances to/from JSON.
#          Contains TWO serializers:
#            1. WorkoutSerializer     → For the global workout catalogue (Workout model)
#            2. UserWorkoutSerializer → For personal workout log entries (UserWorkout model)
#                                       Includes DYNAMIC CALORIE CALCULATION via to_representation()
#
# KEY FEATURE — Dynamic Calorie Calculation in UserWorkoutSerializer:
#   Calories are NOT stored in the UserWorkout table.
#   Instead, they are computed in real-time when the API returns data:
#     actual_calories = base_workout.calories_burned × (user_duration / base_workout.duration_minutes)
#   EXAMPLE:
#     Base workout "Running": calories_burned=500, duration_minutes=60
#     User logged: duration=30 minutes
#     Ratio = 30 / 60 = 0.5
#     Actual calories burned = 500 × 0.5 = 250 kcal
#   This dynamic approach means calorie values automatically update if the base workout data changes.
# ===================================================================================================================

from rest_framework import serializers      # DRF base serializer module
from .models import Workout, UserWorkout    # Import both models from workouts/models.py


class WorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for the Workout global catalogue model.
    Used by workouts_list() to return the full exercise catalogue to Flutter.
    Simple serializer: exposes all fields, no custom logic needed.
    """

    class Meta:
        model = Workout       # Maps to the workouts_workout database table
        fields = '__all__'    # Exposes all columns: id, name, category, duration_minutes, calories_burned


class UserWorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserWorkout personal log model.
    Adds 3 read-only computed fields that pull data from the related Workout catalogue entry.
    Overrides to_representation() to inject the dynamically calculated calorie value.
    """

    # SerializerMethodField alternative: these use source= to traverse the ForeignKey relationship.
    # source='workout.name' → accesses the related Workout object's 'name' field
    # read_only=True → these fields are NEVER accepted from the client; they are always computed server-side
    # When Flutter receives a UserWorkout log, it gets the workout name without a separate API call.
    workout_name = serializers.CharField(source='workout.name', read_only=True)

    # source='workout.category' → reads the category from the linked Workout catalogue entry
    # Example: "Chest", "Cardio", "Back"
    category = serializers.CharField(source='workout.category', read_only=True)

    # Placeholder field for calories_burned. The actual value is overwritten in to_representation().
    # read_only=True → client cannot set this value; it is always computed dynamically
    calories_burned = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserWorkout  # Maps to the workouts_userworkout database table
        # Explicit field list — only expose the fields Flutter needs:
        # id            → unique log entry ID (primary key)
        # workout       → the ForeignKey ID of the catalogue workout
        # workout_name  → computed from workout.name (read_only)
        # category      → computed from workout.category (read_only)
        # date          → auto-set to today when the log is created
        # duration      → actual minutes the user worked out (provided by client)
        # calories_burned → dynamically calculated in to_representation()
        fields = ['id', 'workout', 'workout_name', 'category', 'date', 'duration', 'calories_burned']

    def to_representation(self, instance):
        """
        Called automatically by DRF when converting a UserWorkout instance to a JSON-serializable dict.
        Overrides the default behavior to inject the dynamically calculated calorie value.

        HOW IT WORKS:
          1. Call the parent's to_representation() to get the base dict with all field values
          2. Access the related Workout catalogue entry via instance.workout
          3. Compute the calorie ratio: user_duration / base_duration_minutes
          4. Multiply base calories by the ratio → proportional calorie burn
          5. Inject the result into the 'calories_burned' key of the response dict
        """
        # Get the base serialized dict from the parent ModelSerializer
        ret = super().to_representation(instance)

        # Access the related Workout catalogue entry (traverses the ForeignKey)
        # instance.workout → the Workout object linked to this UserWorkout log
        base_workout = instance.workout

        # Compute the ratio of actual duration to reference duration.
        # Guard against division by zero: if base duration is 0 (bad data), default ratio to 1.0
        # Example: user did 45 min, base is 60 min → ratio = 45/60 = 0.75
        ratio = instance.duration / base_workout.duration_minutes if base_workout.duration_minutes > 0 else 1.0

        # Compute and inject the proportional calorie burn into the response dict.
        # int() rounds down to a whole number (kcal displayed as integer in the Flutter UI)
        # Example: base 300 kcal × 0.75 ratio = 225 kcal
        ret['calories_burned'] = int(base_workout.calories_burned * ratio)

        return ret  # Return the modified dict → DRF converts it to JSON and sends to Flutter
