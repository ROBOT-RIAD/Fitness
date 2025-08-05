from django.db import models
from accounts.models import User
from workout.models import Workout
from datetime import date


class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    workout_plan_name = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for the meal plan")
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s workout plan ({self.start_date} to {self.end_date})"
    

    def mark_complete_if_expired(self):
        if date.today() > self.end_date and not self.is_completed:
            self.is_completed = True
            self.save()
    



class DailyWorkout(models.Model):
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='daily_workouts')
    date = models.DateField()
    title = models.CharField(max_length=255, help_text="Title for the daily workout")
    title_spanish = models.CharField(max_length=255, blank=True, help_text="Título del entrenamiento diario en español")
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")
    tags_spanish = models.CharField(max_length=255, blank=True, help_text="Etiquetas separadas por comas en español")
    completed = models.BooleanField(default=False, help_text="Mark if the workout is completed")

    def __str__(self):
        return f"{self.title} on {self.date} for {self.workout_plan.user.email}"




class WorkoutEntry(models.Model):
    daily_workout = models.ForeignKey(DailyWorkout, on_delete=models.CASCADE, related_name='workouts')
    workout = models.ForeignKey(Workout, to_field='unique_id', on_delete=models.SET_NULL, null=True, blank=True)
    completed = models.BooleanField(default=False)
    set_of = models.PositiveIntegerField(default=1, help_text="Number of sets performed")
    reps = models.PositiveIntegerField(default=10, help_text="Repetitions per set") 

    def __str__(self):
        workout_name = self.workout.workout_name if self.workout else "Unknown Workout"
        return f"{workout_name} on {self.daily_workout.date} - Sets: {self.set_of} - Completed: {self.completed}" 


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        all_completed = self.daily_workout.workouts.filter(completed=False).count() == 0
        if all_completed and not self.daily_workout.completed:
            self.daily_workout.completed = True
            self.daily_workout.save()
        elif not all_completed and self.daily_workout.completed:
            self.daily_workout.completed = False
            self.daily_workout.save()



  