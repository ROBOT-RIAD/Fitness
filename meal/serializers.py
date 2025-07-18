from rest_framework import serializers
from .models import MealPlan, DailyMeal, MealEntry
from recipe.models import Recipe ,RecipeSpanish



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









class DaywiseRecipeMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['image', 'calories']


class DaywiseMealEntrySerializer(serializers.ModelSerializer):
    recipe = DaywiseRecipeMinimalSerializer()

    class Meta:
        model = MealEntry
        fields = ['meal_type', 'recipe']


class DaywiseDailyMealSerializer(serializers.ModelSerializer):
    meals = DaywiseMealEntrySerializer(many=True)

    class Meta:
        model = DailyMeal
        fields = ['id','date', 'meals']






class FullRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class MealEntryWithFullRecipeSerializer(serializers.ModelSerializer):
    recipe = FullRecipeSerializer()

    class Meta:
        model = MealEntry
        fields = ['meal_type', 'recipe']

class RecipeSpanishSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeSpanish
        fields = '__all__'




class MealEntryWithFullRecipeSpanishSerializer(serializers.ModelSerializer):
    recipe = serializers.SerializerMethodField()

    class Meta:
        model = MealEntry
        fields = ['meal_type', 'recipe']

    def get_recipe(self, obj):
        from recipe.models import RecipeSpanish
        if obj.recipe and obj.recipe.unique_id:
            try:
                recipe_sp = RecipeSpanish.objects.get(unique_id=obj.recipe.unique_id)
                return RecipeSpanishSerializer(recipe_sp).data
            except RecipeSpanish.DoesNotExist:
                return None
        return None






