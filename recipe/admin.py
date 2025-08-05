from django.contrib import admin
from .models import Recipe, RecipeSpanish


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'unique_id', 'recipe_name', 'recipe_type', 'for_time', 'tag',
        'calories', 'carbs', 'protein', 'fat', 'making_time', 'time',
        'ratings', 'category', 'created_at', 'updated_at'
    )
    search_fields = ('recipe_name', 'tag', 'category')
    list_filter = ('recipe_type', 'category', 'for_time')
    readonly_fields = ('created_at', 'updated_at')




@admin.register(RecipeSpanish)
class RecipeSpanishAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'unique_id', 'recipe_name', 'recipe_type', 'for_time', 'tag',
        'calories', 'carbs', 'protein', 'fat', 'making_time', 'time',
        'ratings', 'category', 'created_at', 'updated_at'
    )
    search_fields = ('recipe_name', 'tag', 'category')
    list_filter = ('recipe_type', 'category', 'for_time')
    readonly_fields = ('created_at', 'updated_at')
