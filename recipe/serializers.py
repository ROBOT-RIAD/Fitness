from rest_framework import serializers
from .models import Recipe,RecipeSpanish



class ExtendedFileField(serializers.FileField):
    def to_representation(self, value):
        if value:
            request = self.context.get('request')
            url = getattr(value, 'url', value)
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None




class RecipeSerializer(serializers.ModelSerializer):
    image = ExtendedFileField(required=False)
    class Meta:
        model = Recipe
        fields = ['id', 'unique_id', 'image', 'recipe_name', 'recipe_type', 'tag', 'calories', 'carbs', 'protein', 'fat', 'making_time', 'time', 'ratings', 'category', 'for_time', 'ingredients', 'instructions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {'unique_id': {'required': False}}




class RecipeSpanishSerializer(serializers.ModelSerializer):
    image = ExtendedFileField(required=False)
    class Meta:
        model = RecipeSpanish
        fields = ['id', 'unique_id', 'image', 'recipe_name', 'recipe_type', 'tag', 'calories', 'carbs', 'protein', 'fat', 'making_time', 'time', 'ratings', 'category', 'for_time', 'ingredients', 'instructions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {'unique_id': {'required': False}}

