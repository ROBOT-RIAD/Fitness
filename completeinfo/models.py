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

    # Fields to track when the profile was created and last updated
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set to the current timestamp whenever the object is updated

    def __str__(self):
        return f"Fitness Profile for {self.user.email if self.user else 'Unknown User'} (Weight: {self.current_weight}kg, Feeling: {self.feeling})"
    
    class Meta:
        verbose_name = 'Fitness Profile'
        verbose_name_plural = 'Fitness Profiles'



class Achievement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='achievement')
    # Fields for percentage change
    weight_change = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight change in kg")
    abdominal_change = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage change in abdominal measurements")
    sacrolic_change = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage change in sacrolic measurements")
    subscapularis_change = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage change in subscapularis measurements")
    triceps_change = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage change in triceps measurements")
    
    # Boolean fields to track if the changes are an increase or decrease
    weight_increase = models.BooleanField(default=False, help_text="True if Weight measurement is an increase, False for decrease")
    abdominal_increase = models.BooleanField(default=False, help_text="True if abdominal measurement is an increase, False for decrease")
    sacrolic_increase = models.BooleanField(default=False, help_text="True if sacrolic measurement is an increase, False for decrease")
    subscapularis_increase = models.BooleanField(default=False, help_text="True if subscapularis measurement is an increase, False for decrease")
    triceps_increase = models.BooleanField(default=False, help_text="True if triceps measurement is an increase, False for decrease")
    
    # This can store the date or a flag if the achievement has been reached
    achievement_date = models.DateField(auto_now=True)
    
    # Tracking create and update times
    create_time = models.DateTimeField(auto_now_add=True, help_text="Time when the achievement was created")
    update_time = models.DateTimeField(auto_now=True, help_text="Time when the achievement was last updated")
    
    def __str__(self):
        return f"Achievement for {self.user.username} on {self.achievement_date}"

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

