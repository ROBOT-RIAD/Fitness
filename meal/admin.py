from django.contrib import admin
from .models import MealPlan, DailyMeal, MealEntry

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('meal_plan_name', 'user', 'start_date', 'end_date', 'is_completed', 'is_cancelled', 'created_at')
    list_filter = ('is_completed', 'is_cancelled', 'start_date', 'end_date')
    search_fields = ('meal_plan_name', 'user__email', 'tags')




@admin.register(DailyMeal)
class DailyMealAdmin(admin.ModelAdmin):
    list_display = ('meal_plan', 'date')
    list_filter = ('date',)
    search_fields = ('meal_plan__meal_plan_name', 'meal_plan__user__email')




@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ('daily_meal', 'meal_type', 'recipe', 'completed', 'created_at')
    list_filter = ('meal_type', 'completed', 'created_at')
    search_fields = ('meal_type', 'daily_meal__meal_plan__meal_plan_name', 'recipe__recipe_name')
