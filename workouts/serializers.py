from rest_framework import serializers
from .models import Workout, UserWorkout

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'

class UserWorkoutSerializer(serializers.ModelSerializer):
    workout_name = serializers.CharField(source='workout.name', read_only=True)
    category = serializers.CharField(source='workout.category', read_only=True)
    calories_burned = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = UserWorkout
        fields = ['id', 'workout', 'workout_name', 'category', 'date', 'duration', 'calories_burned']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        base_workout = instance.workout
        ratio = instance.duration / base_workout.duration_minutes if base_workout.duration_minutes > 0 else 1.0
        ret['calories_burned'] = int(base_workout.calories_burned * ratio)
        return ret
