
# Create your views here.
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Recipe,RecipeSpanish
from .serializers import RecipeSerializer,RecipeSpanishSerializer
from accounts.permissions import IsAdminRole
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
# Create your views here.
from .translate import translate_to_english,translate_to_spanish




#openai
import openai
openai.api_key = settings.OPENAI_API_KEY
import json


#swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid


def ensure_unique_id(data: dict) -> str:
    """
    Guarantee there is a unique_id in `data` and return it.
    If the client did not send one, generate a fresh UUID‑4.
    """
    if not data.get("unique_id"):
        data["unique_id"] = str(uuid.uuid4())
    return data["unique_id"]




class RecipeAdminViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['recipe_name']
    filterset_fields = ['for_time']
    pagination_class = CustomPageNumberPagination
    parser_classes = [MultiPartParser, FormParser]


    @swagger_auto_schema(operation_summary="List all English recipes (Admin only)", tags=["Recipe"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary="Retrieve an English recipe by ID (Admin only)", tags=["Recipe"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary="Create a new English recipe (Admin only)", tags=["Recipe"])
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        ensure_unique_id(data)
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()


        translatable_fields = {
            'recipe_name': recipe.recipe_name,
            'recipe_type': recipe.recipe_type,
            'for_time': recipe.for_time,
            'tag': recipe.tag,
            'category': recipe.category,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
        }


        try:
            translated_data = translate_to_spanish(translatable_fields)
            spanish_data = {
                'unique_id': recipe.unique_id,
                'image': recipe.image if recipe.image else None,
                'recipe_name': translated_data.get('recipe_name', recipe.recipe_name),
                'recipe_type': translated_data.get('recipe_type', recipe.recipe_type),
                'for_time': translated_data.get('for_time', recipe.for_time),
                'tag': translated_data.get('tag', recipe.tag),
                'calories': recipe.calories,
                'carbs': recipe.carbs,
                'protein': recipe.protein,
                'fat': recipe.fat,
                'making_time': recipe.making_time,
                'time': recipe.time,
                'ratings': recipe.ratings,
                'category': translated_data.get('category', recipe.category),
                'ingredients': translated_data.get('ingredients', recipe.ingredients),
                'instructions': translated_data.get('instructions', recipe.instructions),
            }


            spanish_serializer = RecipeSpanishSerializer(data=spanish_data)
            spanish_serializer.is_valid(raise_exception=True)
            spanish_recipe = spanish_serializer.save()
            recipe.related_recipe = spanish_recipe
            recipe.save()


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            recipe.delete()
            return Response({"error": f"Failed to save translated recipe: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_summary="Update an English recipe (Admin only)", tags=["Recipe"])
    def update(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated_recipe = serializer.save()


        translatable_fields = {
            'recipe_name': updated_recipe.recipe_name,
            'recipe_type': updated_recipe.recipe_type,
            'for_time': updated_recipe.for_time,
            'tag': updated_recipe.tag,
            'category': updated_recipe.category,
            'ingredients': updated_recipe.ingredients,
            'instructions': updated_recipe.instructions,
        }


        try:
            translated_data = translate_to_spanish(translatable_fields)
            spanish_data = {
                'unique_id': updated_recipe.unique_id,
                'image': updated_recipe.image if updated_recipe.image else None,
                'recipe_name': translated_data.get('recipe_name', updated_recipe.recipe_name),
                'recipe_type': translated_data.get('recipe_type', updated_recipe.recipe_type),
                'for_time': translated_data.get('for_time', updated_recipe.for_time),
                'tag': translated_data.get('tag', updated_recipe.tag),
                'calories': updated_recipe.calories,
                'carbs': updated_recipe.carbs,
                'protein': updated_recipe.protein,
                'fat': updated_recipe.fat,
                'making_time': updated_recipe.making_time,
                'time': updated_recipe.time,
                'ratings': updated_recipe.ratings,
                'category': translated_data.get('category', updated_recipe.category),
                'ingredients': translated_data.get('ingredients', updated_recipe.ingredients),
                'instructions': translated_data.get('instructions', updated_recipe.instructions),
            }


            spanish_recipe = recipe.related_recipe
            if spanish_recipe:
                spanish_serializer = RecipeSpanishSerializer(spanish_recipe, data=spanish_data, partial=False)
                spanish_serializer.is_valid(raise_exception=True)
                spanish_serializer.save()
            else:
                spanish_serializer = RecipeSpanishSerializer(data=spanish_data)
                spanish_serializer.is_valid(raise_exception=True)
                spanish_recipe = spanish_serializer.save()
                updated_recipe.related_recipe = spanish_recipe
                updated_recipe.save()


            return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"Failed to update translated recipe: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_summary="Partially update an English recipe (Admin only)", tags=["Recipe"])
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary="Delete an English recipe (Admin only)", tags=["Recipe"])
    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeSpanishAdminViewSet(ModelViewSet):
    queryset = RecipeSpanish.objects.all()
    serializer_class = RecipeSpanishSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['recipe_name']
    filterset_fields = ['for_time']
    pagination_class = CustomPageNumberPagination
    parser_classes = [MultiPartParser, FormParser]


    @swagger_auto_schema(operation_summary="List all Spanish recipes (Admin only)", tags=["RecipeSpanish"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary="Retrieve a Spanish recipe by ID (Admin only)", tags=["RecipeSpanish"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary="Create a new Spanish recipe (Admin only)", tags=["RecipeSpanish"])
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        ensure_unique_id(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        recipe_spanish = serializer.save()


        translatable_fields = {
            'recipe_name': recipe_spanish.recipe_name,
            'recipe_type': recipe_spanish.recipe_type,
            'for_time': recipe_spanish.for_time,
            'tag': recipe_spanish.tag,
            'category': recipe_spanish.category,
            'ingredients': recipe_spanish.ingredients,
            'instructions': recipe_spanish.instructions,
        }


        try:
            translated_data = translate_to_english(translatable_fields)
            english_data = {
                'unique_id': recipe_spanish.unique_id,
                'image': recipe_spanish.image if recipe_spanish.image else None,
                'recipe_name': translated_data.get('recipe_name', recipe_spanish.recipe_name),
                'recipe_type': translated_data.get('recipe_type', recipe_spanish.recipe_type),
                'for_time': translated_data.get('for_time', recipe_spanish.for_time),
                'tag': translated_data.get('tag', recipe_spanish.tag),
                'calories': recipe_spanish.calories,
                'carbs': recipe_spanish.carbs,
                'protein': recipe_spanish.protein,
                'fat': recipe_spanish.fat,
                'making_time': recipe_spanish.making_time,
                'time': recipe_spanish.time,
                'ratings': recipe_spanish.ratings,
                'category': translated_data.get('category', recipe_spanish.category),
                'ingredients': translated_data.get('ingredients', recipe_spanish.ingredients),
                'instructions': translated_data.get('instructions', recipe_spanish.instructions),
            }


            english_serializer = RecipeSerializer(data=english_data)
            english_serializer.is_valid(raise_exception=True)
            english_recipe = english_serializer.save()
            english_recipe.related_recipe = recipe_spanish
            english_recipe.save()


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            recipe_spanish.delete()
            return Response({"error": f"Failed to save translated recipe: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_summary="Update a Spanish recipe (Admin only)", tags=["RecipeSpanish"])
    def update(self, request, *args, **kwargs):
        recipe_spanish = self.get_object()
        serializer = self.get_serializer(recipe_spanish, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated_recipe_spanish = serializer.save()


        translatable_fields = {
            'recipe_name': updated_recipe_spanish.recipe_name,
            'recipe_type': updated_recipe_spanish.recipe_type,
            'for_time': updated_recipe_spanish.for_time,
            'tag': updated_recipe_spanish.tag,
            'category': updated_recipe_spanish.category,
            'ingredients': updated_recipe_spanish.ingredients,
            'instructions': updated_recipe_spanish.instructions,
        }


        try:
            translated_data = translate_to_english(translatable_fields)
            english_data = {
                'unique_id': updated_recipe_spanish.unique_id,
                'image': updated_recipe_spanish.image if updated_recipe_spanish.image else None,
                'recipe_name': translated_data.get('recipe_name', updated_recipe_spanish.recipe_name),
                'recipe_type': translated_data.get('recipe_type', updated_recipe_spanish.recipe_type),
                'for_time': translated_data.get('for_time', updated_recipe_spanish.for_time),
                'tag': translated_data.get('tag', updated_recipe_spanish.tag),
                'calories': updated_recipe_spanish.calories,
                'carbs': updated_recipe_spanish.carbs,
                'protein': updated_recipe_spanish.protein,
                'fat': updated_recipe_spanish.fat,
                'making_time': updated_recipe_spanish.making_time,
                'time': updated_recipe_spanish.time,
                'ratings': updated_recipe_spanish.ratings,
                'category': translated_data.get('category', updated_recipe_spanish.category),
                'ingredients': translated_data.get('ingredients', updated_recipe_spanish.ingredients),
                'instructions': translated_data.get('instructions', updated_recipe_spanish.instructions),
            }


            english_recipe = getattr(recipe_spanish, 'recipe', None)
            if english_recipe:
                english_serializer = RecipeSerializer(english_recipe, data=english_data, partial=False)
                english_serializer.is_valid(raise_exception=True)
                english_serializer.save()
            else:
                english_serializer = RecipeSerializer(data=english_data)
                english_serializer.is_valid(raise_exception=True)
                english_recipe = english_serializer.save()
                english_recipe.related_recipe = recipe_spanish
                english_recipe.save()


            return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"Failed to update translated recipe: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(operation_summary="Partially update a Spanish recipe (Admin only)", tags=["RecipeSpanish"])
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary="Delete a Spanish recipe (Admin only)", tags=["RecipeSpanish"])
    def destroy(self, request, *args, **kwargs):
        recipe_spanish = self.get_object()
        recipe_spanish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


