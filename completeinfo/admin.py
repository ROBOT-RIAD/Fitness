from django.contrib import admin
from .models import FitnessProfile,Achievement


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




class AchievementAdmin(admin.ModelAdmin):
    # Exclude non-editable fields like 'create_time', 'update_time', and 'achievement_date'
    exclude = ('create_time', 'update_time', 'achievement_date')

    # Optionally, you can specify the fields you want to display in the form
    fields = ['user', 'weight_change', 'abdominal_change', 'sacrolic_change', 
              'subscapularis_change', 'triceps_change', 'weight_increase', 
              'abdominal_increase', 'sacrolic_increase', 'subscapularis_increase', 
              'triceps_increase']

    # You can also specify which fields are displayed in the list view
    list_display = ['user', 'weight_change', 'abdominal_change', 'sacrolic_change', 
                    'subscapularis_change', 'triceps_change', 'achievement_date']
    
  
    

# Register the FitnessProfile model with custom admin
admin.site.register(FitnessProfile, FitnessProfileAdmin)
admin.site.register(Achievement, AchievementAdmin)
