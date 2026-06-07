from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Workout, UserWorkout
from .serializers import WorkoutSerializer, UserWorkoutSerializer
import datetime

@api_view(['GET'])
def workouts_list(request):
    workouts = Workout.objects.all()
    serializer = WorkoutSerializer(workouts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_workout_history(request):
    if request.method == 'GET':
        # BUG FIX: support optional ?date=YYYY-MM-DD filter for per-day stats
        date_param = request.GET.get('date', None)
        qs = UserWorkout.objects.filter(user=request.user)
        if date_param:
            try:
                target_date = datetime.date.fromisoformat(date_param)
                qs = qs.filter(date=target_date)
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        history = qs.order_by('-date')
        serializer = UserWorkoutSerializer(history, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        data = request.data.copy()
        workout_id = data.get('workout')
        if not workout_id:
            workout_name = data.get('workout_name', 'Workout')
            category = data.get('category', 'General')
            duration = data.get('duration', 30)
            
            workout, _ = Workout.objects.get_or_create(
                name=workout_name,
                category=category,
                defaults={
                    'duration_minutes': duration,
                    'calories_burned': 250
                }
            )
            data['workout'] = workout.id
            
        serializer = UserWorkoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_workout_history(request):
    UserWorkout.objects.filter(user=request.user).delete()
    return Response({"message": "Workout history cleared successfully!"}, status=200)