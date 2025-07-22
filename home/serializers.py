from rest_framework import serializers
from meal.models import MealEntry, DailyMeal
from workoutplan.models import WorkoutEntry, DailyWorkout
from datetime import datetime, time
from AiChat.models import HealthProfile

class MealEntrySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealEntry
        fields = ['meal_type', 'eating_time', 'completed']


class DailyMealTodaySerializer(serializers.ModelSerializer):
    entries = MealEntrySimpleSerializer(source='meals', many=True)

    class Meta:
        model = DailyMeal
        fields = ['date', 'entries']


class WorkoutEntrySimpleSerializer(serializers.ModelSerializer):
    workout_name = serializers.CharField(source='workout.workout_name', default=None)

    class Meta:
        model = WorkoutEntry
        fields = ['workout_name', 'set_of', 'reps', 'completed']


class DailyWorkoutTodaySerializer(serializers.ModelSerializer):
    entries = WorkoutEntrySimpleSerializer(source='workouts', many=True)

    class Meta:
        model = DailyWorkout
        fields = ['date','entries']


class AIRecommendedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfile
        fields = [
            'water_need_liters_per_day',
            'sleep_need_hours_per_day',
            'total_calories_per_day',
            'perfect_weight_kg',
        ]
