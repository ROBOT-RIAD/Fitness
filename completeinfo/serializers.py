from rest_framework import serializers
from .models import FitnessProfile
from meal.models import MealPlan
from workoutplan.models import WorkoutPlan

class FitnessProfileSerializer(serializers.ModelSerializer):
    meal_plan = serializers.PrimaryKeyRelatedField(queryset=MealPlan.objects.all(), required=False, allow_null=True)
    workout_plan = serializers.PrimaryKeyRelatedField(queryset=WorkoutPlan.objects.all(), required=False, allow_null=True)

    class Meta:
        model = FitnessProfile
        fields = ["user", 'current_weight', 'abdominal', 'sacroiliac', 'subscapularis', 'triceps', 
                  'feeling', 'total_meal', 'workout_consistency', 'energy_level', 'injuries_pain', 
                  'meal_plan', 'workout_plan', 'created_at', 'updated_at']
        read_only_fields = ["user", 'created_at', 'updated_at']

    # Optionally, you can add validations if required
    def validate_current_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0.")
        return value
