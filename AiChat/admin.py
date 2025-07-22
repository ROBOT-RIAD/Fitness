from django.contrib import admin
from .models import HealthProfile

# Register your models here.

@admin.register(HealthProfile)
class HealthProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'perfect_weight_kg',
        'total_calories_per_day',
        'water_need_liters_per_day',
        'sleep_need_hours_per_day',
        'created_at',
        'updated_at',
    )
    search_fields = ('user__username',)
    list_filter = ('created_at', 'updated_at')