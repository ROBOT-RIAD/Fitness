from rest_framework import serializers
from meal.models import MealEntry, DailyMeal
from workoutplan.models import WorkoutEntry, DailyWorkout
from datetime import datetime, time
from AiChat.models import HealthProfile
from workout.models import WorkoutSpanish


MEAL_TYPE_TRANSLATIONS = {
    "Breakfast": "Desayuno",
    "Snack": "Merienda",
    "Snack 1": "Merienda 1",
    "Lunch": "Almuerzo",
    "Snack 2": "Merienda 2",
    "Dinner": "Cena",
    "Snack 3": "Merienda 3",
    "Post-Dinner": "Después de la cena",
    "Late Snack": "Merienda nocturna"
}



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




# //spanish hoime
class SpanishMealEntrySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealEntry
        fields = ['meal_type', 'eating_time', 'completed']

    def to_representation(self, instance):
        # Get the original representation
        representation = super().to_representation(instance)

        # Translate the meal_type to Spanish if it exists in the dictionary
        meal_type = representation.get('meal_type', '')
        if meal_type in MEAL_TYPE_TRANSLATIONS:
            representation['meal_type'] = MEAL_TYPE_TRANSLATIONS[meal_type]

        return representation
    



class SpanishDailyMealTodaySerializer(serializers.ModelSerializer):
    entries = SpanishMealEntrySimpleSerializer(source='meals', many=True)

    class Meta:
        model = DailyMeal
        fields = ['date', 'entries']




class SpanishWorkoutEntrySimpleSerializer(serializers.ModelSerializer):
    workout_name_spanish = serializers.SerializerMethodField()
   

    class Meta:
        model = WorkoutEntry
        fields = ['workout_name_spanish', 'set_of', 'reps', 'completed']

    def get_workout_name_spanish(self, obj):
        workout = obj.workout
        if workout:
            spanish_workout = WorkoutSpanish.objects.filter(unique_id=workout.unique_id).first()
            if spanish_workout:
                return spanish_workout.workout_name
        return None
    


    
class SpanishDailyWorkoutTodaySerializer(serializers.ModelSerializer):
    entries = SpanishWorkoutEntrySimpleSerializer(source='workouts', many=True)

    class Meta:
        model = DailyWorkout
        fields = ['date', 'entries']
