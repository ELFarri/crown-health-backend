# foods/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Food
from .serializers import FoodSerializer

@api_view(['GET'])
def food_list(request):
    foods = Food.objects.all()[:10]
    serializer = FoodSerializer(foods, many=True)
    return Response({
        'success': True,
        'count': foods.count(),
        'foods': serializer.data
    })

@api_view(['GET'])
def food_search(request):
    query = request.GET.get('q', '')
    if query:
        foods = Food.objects.filter(name__icontains=query)[:5]
    else:
        foods = Food.objects.none()
    serializer = FoodSerializer(foods, many=True)
    return Response(serializer.data)