import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calal_backend.settings')
django.setup()

from users.models import CustomUser

def create_users():
    users_data = [
        {
            'username': 'sarah@test.com',
            'email': 'sarah@test.com',
            'name': 'Sarah',
            'password': 'password123',
            'age': 24,
            'gender': 'female',
            'height': 165.0,
            'weight': 72.0,
            'goal': 'loss',
            'activity_level': 'active',
        },
        {
            'username': 'marc@test.com',
            'email': 'marc@test.com',
            'name': 'Marc',
            'password': 'password123',
            'age': 30,
            'gender': 'male',
            'height': 185.0,
            'weight': 80.0,
            'goal': 'gain',
            'activity_level': 'very_active',
        },
        {
            'username': 'lea@test.com',
            'email': 'lea@test.com',
            'name': 'Léa',
            'password': 'password123',
            'age': 28,
            'gender': 'female',
            'height': 160.0,
            'weight': 55.0,
            'goal': 'maintain',
            'activity_level': 'sedentary',
        },
        {
            'username': 'thomas@test.com',
            'email': 'thomas@test.com',
            'name': 'Thomas',
            'password': 'password123',
            'age': 22,
            'gender': 'male',
            'height': 178.0,
            'weight': 95.0,
            'goal': 'loss',
            'activity_level': 'moderate',
        }
    ]

    for data in users_data:
        if not CustomUser.objects.filter(username=data['username']).exists():
            user = CustomUser.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                name=data['name'],
                age=data['age'],
                gender=data['gender'],
                height=data['height'],
                weight=data['weight'],
                goal=data['goal'],
                activity_level=data['activity_level']
            )
            print(f"User {user.name} created successfully.")
        else:
            print(f"User {data['name']} already exists.")

if __name__ == '__main__':
    create_users()
