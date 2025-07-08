from django.db import models
from accounts.models import User
from workout.models import Workout



class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s workout plan ({self.start_date} to {self.end_date})"
    





class DailyWorkout(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='daily_workouts')
    date = models.DateField()

    def __str__(self):
        return f"Workout on {self.date} for {self.workout_plan.user.email}"
    





class WorkoutEntry(models.Model):
    daily_workout = models.ForeignKey(DailyWorkout, on_delete=models.CASCADE, related_name='workouts')
    workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.workout.workout_name} on {self.daily_workout.date} - Completed: {self.completed}"