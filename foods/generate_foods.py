import json
import random

# Expanded food database
foods = [
    # Vegetables
    ("Broccoli", "Vegetable", 34, 2.8, 6.6, 0.4, 2.6, 1.7),
    ("Carrot", "Vegetable", 41, 0.9, 9.6, 0.2, 2.8, 4.7),
    ("Spinach", "Vegetable", 23, 2.9, 3.6, 0.4, 2.2, 0.4),
    ("Tomato", "Vegetable", 18, 0.9, 3.9, 0.2, 1.2, 2.6),
    ("Cucumber", "Vegetable", 15, 0.7, 3.6, 0.1, 0.5, 1.7),

    # Fruits
    ("Apple", "Fruit", 52, 0.3, 14, 0.2, 2.4, 10),
    ("Banana", "Fruit", 89, 1.1, 23, 0.3, 2.6, 12),
    ("Orange", "Fruit", 47, 0.9, 12, 0.1, 2.4, 9),
    ("Mango", "Fruit", 60, 0.8, 15, 0.4, 1.6, 14),
    ("Strawberry", "Fruit", 32, 0.7, 8, 0.3, 2, 4.9),

    # Protein
    ("Chicken Breast", "Protein", 165, 31, 0, 3.6, 0, 0),
    ("Egg", "Protein", 155, 13, 1.1, 11, 0, 1.1),
    ("Salmon", "Protein", 208, 20, 0, 13, 0, 0),
    ("Tuna", "Protein", 132, 28, 0, 1, 0, 0),
    ("Beef", "Protein", 250, 26, 0, 15, 0, 0),

    # Carbs
    ("Rice", "Carbohydrates", 130, 2.4, 28, 0.3, 0.4, 0),
    ("Bread", "Carbohydrates", 265, 9, 49, 3.2, 2.4, 5),
    ("Pasta", "Carbohydrates", 131, 5, 25, 1.1, 1.5, 1),
    ("Oats", "Carbohydrates", 389, 17, 66, 7, 10, 1),
    ("Potato", "Carbohydrates", 77, 2, 17, 0.1, 2.2, 0.8),

    # Fats
    ("Avocado", "Fats", 160, 2, 9, 15, 7, 0.7),
    ("Olive Oil", "Fats", 884, 0, 0, 100, 0, 0),
    ("Butter", "Fats", 717, 0.9, 0.1, 81, 0, 0.1),
    ("Almonds", "Fats", 579, 21, 22, 50, 12, 4.4),

    # Dairy
    ("Milk", "Dairy", 61, 3.2, 4.8, 3.3, 0, 5),
    ("Cheese", "Dairy", 403, 25, 1.3, 33, 0, 0.5),
    ("Yogurt", "Dairy", 59, 10, 3.6, 0.4, 0, 3.2),

    # Sweets
    ("Chocolate", "Sweets", 535, 7.6, 59, 30, 3.4, 52),
    ("Ice Cream", "Sweets", 207, 3.5, 24, 11, 0.7, 21),

    # Beverages
    ("Coffee", "Beverages", 2, 0.3, 0, 0, 0, 0),
    ("Orange Juice", "Beverages", 45, 0.7, 10.4, 0.2, 0.2, 8.4),
    ("Tea", "Beverages", 1, 0, 0, 0, 0, 0),
]

data = []

# Generate 2000 foods
for i in range(2000):
    food = random.choice(foods)

    item = {
        "model": "foods.food",  # ⚠️ change if your app name is different
        "fields": {
            "name": f"{food[0]} {i}",
            "category": food[1],
            "calories": food[2],
            "protein": food[3],
            "carbs": food[4],
            "fat": food[5],
            "fiber": food[6],
            "sugar": food[7]
        }
    }

    data.append(item)

with open("foods_big.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Generated 2000+ foods")