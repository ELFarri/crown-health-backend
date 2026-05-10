"""
foods/models.py - Food database for Calal application
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

class Food(models.Model):
    """
    Food model with all essential nutrients
    """
    
    # Food categories
    CATEGORIES = [
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('proteins', 'Proteins'),
        ('carbs', 'Carbohydrates'),
        ('fats', 'Fats'),
        ('dairy', 'Dairy'),
        ('sweets', 'Sweets'),
        ('beverages', 'Beverages'),
    ]
    
    # Basic data
    name = models.CharField(
        max_length=100, 
        verbose_name=_("Food Name")
    )
    
    brand = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name=_("Brand")
    )
    
    category = models.CharField(
        max_length=20, 
        choices=CATEGORIES,
        blank=True,
        verbose_name=_("Category")
    )
    
    # Nutrients per 100g
    serving_size = models.CharField(
        max_length=50, 
        default='100g',
        verbose_name=_("Serving Size")
    )
    
    calories = models.IntegerField(
        default=0,
        verbose_name=_("Calories")
    )
    
    protein = models.FloatField(
        default=0,
        verbose_name=_("Protein (g)")
    )
    
    carbs = models.FloatField(
        default=0,
        verbose_name=_("Carbs (g)")
    )
    
    fat = models.FloatField(
        default=0,
        verbose_name=_("Fat (g)")
    )
    
    fiber = models.FloatField(
        default=0,
        verbose_name=_("Fiber (g)")
    )
    
    sugar = models.FloatField(
        default=0,
        verbose_name=_("Sugar (g)")
    )
    
    # Additional info
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Description")
    )
    
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Verified")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )
    
    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.calories}cal/100g)"
    
    def get_nutrition_per_serving(self):
        """Get nutrition per serving"""
        return {
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'fiber': self.fiber,
        }

# Sample data for quick testing
class FoodData:
    SAMPLE_FOODS = [
        {
            'name': 'Grilled Chicken',
            'brand': 'Natural',
            'category': 'proteins',
            'calories': 165,
            'protein': 31,
            'carbs': 0,
            'fat': 3.6,
            'fiber': 0,
        },
        {
            'name': 'White Rice',
            'brand': '',
            'category': 'carbs',
            'calories': 130,
            'protein': 2.7,
            'carbs': 28,
            'fat': 0.3,
            'fiber': 0.4,
        },
        {
            'name': 'Apple',
            'brand': '',
            'category': 'fruits',
            'calories': 52,
            'protein': 0.3,
            'carbs': 14,
            'fat': 0.2,
            'fiber': 2.4,
        },
        {
            'name': 'Boiled Egg',
            'brand': '',
            'category': 'proteins',
            'calories': 78,
            'protein': 6.3,
            'carbs': 0.6,
            'fat': 5.3,
            'fiber': 0,
        },
        {
            'name': 'White Bread',
            'brand': '',
            'category': 'carbs',
            'calories': 265,
            'protein': 9,
            'carbs': 49,
            'fat': 3.2,
            'fiber': 2.7,
        },
    ]