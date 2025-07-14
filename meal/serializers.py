from rest_framework import serializers
from .models import MealPlan, DailyMeal, MealEntry
from recipe.models import Recipe   # ← your app name

class MealEntryWriteSerializer(serializers.Serializer):
    meal_type     = serializers.CharField()
    recipe_uid    = serializers.CharField(source='recipe.unique_id')

class DailyMealWriteSerializer(serializers.Serializer):
    date          = serializers.DateField()
    meals         = MealEntryWriteSerializer(many=True)

class MealPlanWriteSerializer(serializers.Serializer):
    meal_plan_name = serializers.CharField(required=False, default='15‑Day AI Plan')
    tags           = serializers.CharField(required=False, allow_blank=True)
    daily_meals    = DailyMealWriteSerializer(many=True)