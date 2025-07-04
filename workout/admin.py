from django.contrib import admin
from .models import Workout
# Register your models here.

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'workout_name', 'workout_type', 'for_body_part',
        'calories_burn', 'time_needed', 'equipment_needed',
        'tag', 'created_at', 'updated_at'
    )
    list_filter = ('for_body_part',)
    search_fields = ('workout_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
