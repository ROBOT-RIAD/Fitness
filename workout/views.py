from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import Workout
from .serializers import WorkoutSerializer
from accounts.permissions import IsAdminRole  # Assuming you placed IsAdminRole there
from .pagination import CustomPageNumberPagination 
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.


class WorkoutAdminViewSet(ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['workout_name']
    filterset_fields = ['for_body_part', 'workout_type']
    pagination_class = CustomPageNumberPagination  
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(operation_summary="List all workouts (Admin only)", tags=["Workout"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a workout by ID (Admin only)", tags=["Workout"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new workout (Admin only)", tags=["Workout"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Update a workout (Admin only)", tags=["Workout"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Partially update a workout (Admin only)", tags=["Workout"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a workout (Admin only)", tags=["Workout"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)