# nutrition/views.py - النسخة المُصححة
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Meal
from .serializers import MealSerializer
from users.models import CustomUser

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meals_list(request):
    meals = Meal.objects.filter(user=request.user)
    serializer = MealSerializer(meals, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_meal(request):
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)