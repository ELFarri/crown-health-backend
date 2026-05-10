from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def workouts_list(request):
    return Response({"workouts": "API ready"})

@api_view(['POST'])
def add_workout(request):
    return Response({"message": "Workout added"})