from django.contrib import admin
from .models import Workout, WorkoutSpanish


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'unique_id',
        'workout_name',
        'workout_type',
        'for_body_part',
        'calories_burn',
        'time_needed',
        'equipment_needed',
        'tag',
        'created_at',
        'updated_at',
    )
    search_fields = ('workout_name', 'workout_type', 'for_body_part', 'tag')
    list_filter = ('workout_type', 'for_body_part', 'tag')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WorkoutSpanish)
class WorkoutSpanishAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'unique_id',
        'workout_name',
        'workout_type',
        'for_body_part',
        'calories_burn',
        'time_needed',
        'equipment_needed',
        'tag',
        'created_at',
        'updated_at',
    )
    search_fields = ('workout_name', 'workout_type', 'for_body_part', 'tag')
    list_filter = ('workout_type', 'for_body_part', 'tag')
    readonly_fields = ('created_at', 'updated_at')
