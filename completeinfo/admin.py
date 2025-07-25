from django.contrib import admin
from .models import FitnessProfile

# Customize the admin interface for FitnessProfile
class FitnessProfileAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('user', 'current_weight', 'feeling', 'total_meal', 'workout_consistency', 'energy_level', 'created_at', 'updated_at')

    # Add fields for detail view
    fieldsets = (
        (None, {
            'fields': ('user', 'current_weight', 'abdominal', 'sacroiliac', 'subscapularis', 'triceps', 'feeling')
        }),
        ('Meal & Workout Details', {
            'fields': ('meal_plan', 'workout_plan', 'total_meal', 'workout_consistency', 'energy_level')
        }),
        ('Health Info', {
            'fields': ('injuries_pain',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # This makes the timestamps collapsible
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

# Register the FitnessProfile model with custom admin
admin.site.register(FitnessProfile, FitnessProfileAdmin)
