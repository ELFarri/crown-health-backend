from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import CustomUserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "User registered successfully!",
            "user_id": user.id
        }, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    print(f"Login attempt: {request.data}")
    username = request.data.get('username') or request.data.get('email')
    password = request.data.get('password')
    
    from django.db.models import Q
    user = CustomUser.objects.filter(Q(username=username) | Q(email=username)).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.name
            }
        })
    return Response({"error": "Invalid credentials"}, status=401)

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    user = request.user
    if request.method in ['PUT', 'PATCH']:
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)