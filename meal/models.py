from django.db import models
from datetime import date
from accounts.models import User
from recipe.models import Recipe
# Create your models here.

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    meal_plan_name = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for the meal plan")
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s plan from {self.start_date}"

    def mark_complete_if_expired(self):
        if date.today() > self.end_date and not self.is_completed:
            self.is_completed = True
            self.save()





class DailyMeal(models.Model):
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='daily_meals')
    date = models.DateField()

    def __str__(self):
        return f"Meals on {self.date} for {self.meal_plan.user.email}"
    





class MealEntry(models.Model):
    daily_meal = models.ForeignKey(DailyMeal, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=50)  # Just a plain string now
    recipe = models.ForeignKey(Recipe,to_field='unique_id',on_delete=models.SET_NULL,null=True,blank=True)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.meal_type} on {self.daily_meal.date} - Completed: {self.completed}"



