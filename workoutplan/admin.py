from django.contrib import admin
from .models import WorkoutPlan, DailyWorkout, WorkoutEntry


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'workout_plan_name', 'start_date', 'end_date', 'is_completed', 'is_cancelled')
    list_filter = ('is_completed', 'is_cancelled', 'start_date', 'end_date')
    search_fields = ('workout_plan_name', 'user__email', 'tags')
    date_hierarchy = 'start_date'


@admin.register(DailyWorkout)
class DailyWorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'workout_plan', 'date', 'title', 'completed')
    list_filter = ('completed', 'date')
    search_fields = ('title', 'tags', 'workout_plan__workout_plan_name')


@admin.register(WorkoutEntry)
class WorkoutEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'daily_workout', 'workout', 'set_of', 'reps', 'completed')
    list_filter = ('completed',)
    search_fields = ('daily_workout__title', 'workout__workout_name')

