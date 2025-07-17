from rest_framework import serializers
from accounts.models import Profile
from meal.models import MealPlan
from workoutplan.models import WorkoutPlan


class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'interested_workout', 'fitness_level', 'dietary_preferences', 'weight']


class MealPlanInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = ['id', 'meal_plan_name', 'tags', 'start_date', 'end_date', 'is_completed', 'is_cancelled']


class WorkoutPlanInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = ['id', 'workout_plan_name', 'tags', 'start_date', 'end_date', 'is_completed', 'is_cancelled']


class UserFullInfoSerializer(serializers.Serializer):
    profile = ProfileInfoSerializer()
    meal_plans = MealPlanInfoSerializer(many=True)
    workout_plans = WorkoutPlanInfoSerializer(many=True)
