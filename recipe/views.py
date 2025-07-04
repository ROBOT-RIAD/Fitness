from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Recipe
from .serializers import RecipeSerializer
from accounts.permissions import IsAdminRole
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageNumberPagination
# Create your views here.


#swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RecipeAdminViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['recipe_name']
    filterset_fields = ['for_time']
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(operation_summary="List all recipes (Admin only)", tags=["Recipe"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a recipe by ID (Admin only)", tags=["Recipe"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new recipe (Admin only)", tags=["Recipe"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a recipe (Admin only)", tags=["Recipe"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Partially update a recipe (Admin only)", tags=["Recipe"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a recipe (Admin only)", tags=["Recipe"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)