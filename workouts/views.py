from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Workout, UserWorkout
from .serializers import WorkoutSerializer, UserWorkoutSerializer

@api_view(['GET'])
def workouts_list(request):
    workouts = Workout.objects.all()
    serializer = WorkoutSerializer(workouts, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_workout_history(request):
    if request.method == 'GET':
        history = UserWorkout.objects.filter(user=request.user).order_by('-date')
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