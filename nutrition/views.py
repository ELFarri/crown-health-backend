# nutrition/views.py - النسخة المُصححة
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Meal
from .serializers import MealSerializer
from users.models import CustomUser
from django.utils import timezone
import datetime

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meals_list(request):
    # BUG FIX: filter by date (default = today, optional ?date=YYYY-MM-DD param)
    date_param = request.GET.get('date', None)
    if date_param:
        try:
            target_date = datetime.date.fromisoformat(date_param)
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
    else:
        target_date = timezone.now().date()

    meals = Meal.objects.filter(user=request.user, date=target_date)
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

from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def nutrition_stats(request):
    period = request.GET.get('period', 'weekly')
    today = timezone.now().date()
    
    if period == 'monthly':
        start_date = today - timedelta(days=30)
    else: # weekly default
        start_date = today - timedelta(days=7)
        
    stats = Meal.objects.filter(
        user=request.user,
        date__gte=start_date
    ).values('date').annotate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein'),
        total_carbs=Sum('carbs'),
        total_fat=Sum('fat')
    ).order_by('-date')
    
    return Response(list(stats))