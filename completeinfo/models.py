from django.db import models
from accounts.models import User
from meal.models import MealPlan
from workoutplan.models import WorkoutPlan
# Create your models here.



class FitnessProfile(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='fitness_profiles')
    
    current_weight = models.FloatField(null=True, blank=True)
    abdominal = models.FloatField(null=True, blank=True)
    sacroiliac = models.FloatField(null=True, blank=True)
    subscapularis = models.FloatField(null=True, blank=True)
    triceps = models.FloatField(null=True, blank=True)
    feeling = models.CharField(max_length=100, null=True, blank=True)  # A short description, like "Good", "Tired", etc.
    total_meal = models.IntegerField(null=True, blank=True)  # Number of meals consumed per day
    workout_consistency = models.IntegerField(null=True, blank=True)  # Rating, e.g., 1-5 scale
    energy_level = models.IntegerField(null=True, blank=True)  # Rating, e.g., 1-10 scale
    injuries_pain = models.CharField(max_length=255, null=True, blank=True)  # Describes the injuries/pain level (optional)

    # New optional relationship fields
    meal_plan = models.ForeignKey(MealPlan, null=True, blank=True, on_delete=models.SET_NULL, related_name='fitness_profiles')
    workout_plan = models.ForeignKey(WorkoutPlan, null=True, blank=True, on_delete=models.SET_NULL, related_name='fitness_profiles')

    def __str__(self):
        return f"Fitness Profile for {self.user.email if self.user else 'Unknown User'} (Weight: {self.current_weight}kg, Feeling: {self.feeling})"
    
    class Meta:
        verbose_name = 'Fitness Profile'
        verbose_name_plural = 'Fitness Profiles'