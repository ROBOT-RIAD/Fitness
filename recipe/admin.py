from django.contrib import admin
from .models import Recipe

# Register your models here.



@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'recipe_name', 'recipe_type', 'category', 'for_time',
        'calories', 'carbs', 'protein', 'fat', 'making_time', 'time',
        'ratings', 'created_at', 'updated_at'
    )
    list_filter = ('for_time',)
    search_fields = ('recipe_name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')