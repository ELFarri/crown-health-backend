from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'name', 'age', 'gender', 
                 'height', 'weight', 'goal', 'activity_level']
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)