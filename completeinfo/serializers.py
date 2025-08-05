from rest_framework import serializers
from .models import FitnessProfile,Achievement
from meal.models import MealPlan,MealEntry
from workoutplan.models import WorkoutPlan,WorkoutEntry
from accounts.models import User



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




class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['weight_change', 'abdominal_change', 'sacrolic_change', 'subscapularis_change', 'triceps_change',
                  'weight_increase', 'abdominal_increase', 'sacrolic_increase', 'subscapularis_increase',
                  'triceps_increase', 'achievement_date', 'create_time', 'update_time']




# Serializer for MealPlan model, including total meals completed
class MealPlanSerializer(serializers.ModelSerializer):
    total_meals_completed = serializers.SerializerMethodField()

    class Meta:
        model = MealPlan
        fields = ['meal_plan_name', 'start_date', 'end_date', 'is_completed', 'total_meals_completed']

    def get_total_meals_completed(self, obj):
        return MealEntry.objects.filter(daily_meal__meal_plan=obj, completed=True).count()




# Serializer for WorkoutPlan model, including total workouts completed
class WorkoutPlanSerializer(serializers.ModelSerializer):
    total_workouts_completed = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutPlan
        fields = ['workout_plan_name', 'start_date', 'end_date', 'is_completed', 'total_workouts_completed']

    def get_total_workouts_completed(self, obj):
        return WorkoutEntry.objects.filter(daily_workout__workout_plan=obj, completed=True).count()




# Serializer for User's Achievement, Latest Meal Plan, and Latest Workout Plan
class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()
    latest_meal_plan = serializers.SerializerMethodField()
    latest_workout_plan = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['achievement', 'latest_meal_plan', 'latest_workout_plan']

    def get_latest_meal_plan(self, obj):
        # Get the latest completed MealPlan for the user
        latest_meal_plan = MealPlan.objects.filter(user=obj, is_completed=True).order_by('-end_date').first()
        if latest_meal_plan:
            return MealPlanSerializer(latest_meal_plan).data
        return None

    def get_latest_workout_plan(self, obj):
        # Get the latest completed WorkoutPlan for the user
        latest_workout_plan = WorkoutPlan.objects.filter(user=obj, is_completed=True).order_by('-end_date').first()
        if latest_workout_plan:
            return WorkoutPlanSerializer(latest_workout_plan).data
        return None
    



class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'
