from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from .models import Workout,WorkoutSpanish
from .serializers import WorkoutSerializer,WorkoutSpanishSerializer
from accounts.permissions import IsAdminRole  # Assuming you placed IsAdminRole there
from .pagination import CustomPageNumberPagination 
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.

from recipe.translate import translate_to_english,translate_to_spanish


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

class WorkoutAdminViewSet(ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['workout_name']
    filterset_fields = ['for_body_part', 'workout_type']
    pagination_class = CustomPageNumberPagination
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(operation_summary="List all English workouts (Admin only)", tags=["Workout"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve an English workout by ID (Admin only)", tags=["Workout"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new English workout (Admin only)", tags=["Workout"])
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        ensure_unique_id(data)
        print(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        workout = serializer.save()

        translatable_fields = {
            'workout_name': workout.workout_name,
            'for_body_part': workout.for_body_part,
            'workout_type': workout.workout_type,
            'equipment_needed': workout.equipment_needed,
            'tag': workout.tag,
            'benefits': workout.benefits,
        }

        try:
            translated_data = translate_to_spanish(translatable_fields)
            spanish_data = {
                'unique_id': workout.unique_id,
                'image': workout.image if workout.image else None,
                'workout_name': translated_data.get('workout_name', workout.workout_name),
                'for_body_part': translated_data.get('for_body_part', workout.for_body_part),
                'workout_type': translated_data.get('workout_type', workout.workout_type),
                'calories_burn': workout.calories_burn,
                'time_needed': workout.time_needed,
                'equipment_needed': translated_data.get('equipment_needed', workout.equipment_needed),
                'tag': translated_data.get('tag', workout.tag),
                'benefits': translated_data.get('benefits', workout.benefits),
            }

            spanish_serializer = WorkoutSpanishSerializer(data=spanish_data)
            spanish_serializer.is_valid(raise_exception=True)
            spanish_workout = spanish_serializer.save()
            workout.related_workout = spanish_workout
            workout.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            workout.delete()
            return Response({"error": f"Failed to save translated workout: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Update an English workout (Admin only)", tags=["Workout"])
    def update(self, request, *args, **kwargs):
        workout = self.get_object()
        serializer = self.get_serializer(workout, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated_workout = serializer.save()

        translatable_fields = {
            'workout_name': updated_workout.workout_name,
            'for_body_part': updated_workout.for_body_part,
            'workout_type': updated_workout.workout_type,
            'equipment_needed': updated_workout.equipment_needed,
            'tag': updated_workout.tag,
            'benefits': updated_workout.benefits,
        }

        try:
            translated_data = translate_to_spanish(translatable_fields)
            spanish_data = {
                'unique_id': updated_workout.unique_id,
                'image': updated_workout.image if updated_workout.image else None,
                'workout_name': translated_data.get('workout_name', updated_workout.workout_name),
                'for_body_part': translated_data.get('for_body_part', updated_workout.for_body_part),
                'workout_type': translated_data.get('workout_type', updated_workout.workout_type),
                'calories_burn': updated_workout.calories_burn,
                'time_needed': updated_workout.time_needed,
                'equipment_needed': translated_data.get('equipment_needed', updated_workout.equipment_needed),
                'tag': translated_data.get('tag', updated_workout.tag),
                'benefits': translated_data.get('benefits', updated_workout.benefits),
            }

            spanish_workout = getattr(workout, 'related_workout', None)
            if spanish_workout:
                spanish_serializer = WorkoutSpanishSerializer(spanish_workout, data=spanish_data, partial=False)
                spanish_serializer.is_valid(raise_exception=True)
                spanish_serializer.save()
            else:
                spanish_serializer = WorkoutSpanishSerializer(data=spanish_data)
                spanish_serializer.is_valid(raise_exception=True)
                spanish_workout = spanish_serializer.save()
                updated_workout.related_workout = spanish_workout
                updated_workout.save()

            return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"Failed to update translated workout: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partially update an English workout (Admin only)", tags=["Workout"])
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete an English workout (Admin only)", tags=["Workout"])
    def destroy(self, request, *args, **kwargs):
        workout = self.get_object()
        workout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WorkoutSpanishAdminViewSet(ModelViewSet):
    queryset = WorkoutSpanish.objects.all()
    serializer_class = WorkoutSpanishSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['workout_name']
    filterset_fields = ['for_body_part', 'workout_type']
    pagination_class = CustomPageNumberPagination
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(operation_summary="List all Spanish workouts (Admin only)", tags=["WorkoutSpanish"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Retrieve a Spanish workout by ID (Admin only)", tags=["WorkoutSpanish"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new Spanish workout (Admin only)", tags=["WorkoutSpanish"])
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        ensure_unique_id(data)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        workout_spanish = serializer.save()

        translatable_fields = {
            'workout_name': workout_spanish.workout_name,
            'for_body_part': workout_spanish.for_body_part,
            'workout_type': workout_spanish.workout_type,
            'equipment_needed': workout_spanish.equipment_needed,
            'tag': workout_spanish.tag,
            'benefits': workout_spanish.benefits,
        }

        try:
            translated_data = translate_to_english(translatable_fields)
            english_data = {
                'unique_id': workout_spanish.unique_id,
                'image': workout_spanish.image if workout_spanish.image else None,
                'workout_name': translated_data.get('workout_name', workout_spanish.workout_name),
                'for_body_part': translated_data.get('for_body_part', workout_spanish.for_body_part),
                'workout_type': translated_data.get('workout_type', workout_spanish.workout_type),
                'calories_burn': workout_spanish.calories_burn,
                'time_needed': workout_spanish.time_needed,
                'equipment_needed': translated_data.get('equipment_needed', workout_spanish.equipment_needed),
                'tag': translated_data.get('tag', workout_spanish.tag),
                'benefits': translated_data.get('benefits', workout_spanish.benefits),
            }

            english_serializer = WorkoutSerializer(data=english_data)
            english_serializer.is_valid(raise_exception=True)
            english_workout = english_serializer.save()
            english_workout.related_workout = workout_spanish
            english_workout.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            workout_spanish.delete()
            return Response({"error": f"Failed to save translated workout: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Update a Spanish workout (Admin only)", tags=["WorkoutSpanish"])
    def update(self, request, *args, **kwargs):
        workout_spanish = self.get_object()
        serializer = self.get_serializer(workout_spanish, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated_workout_spanish = serializer.save()

        translatable_fields = {
            'workout_name': updated_workout_spanish.workout_name,
            'for_body_part': updated_workout_spanish.for_body_part,
            'workout_type': updated_workout_spanish.workout_type,
            'equipment_needed': updated_workout_spanish.equipment_needed,
            'tag': updated_workout_spanish.tag,
            'benefits': updated_workout_spanish.benefits,
        }

        try:
            translated_data = translate_to_english(translatable_fields)
            english_data = {
                'unique_id': updated_workout_spanish.unique_id,
                'image': updated_workout_spanish.image if updated_workout_spanish.image else None,
                'workout_name': translated_data.get('workout_name', updated_workout_spanish.workout_name),
                'for_body_part': translated_data.get('for_body_part', updated_workout_spanish.for_body_part),
                'workout_type': translated_data.get('workout_type', updated_workout_spanish.workout_type),
                'calories_burn': updated_workout_spanish.calories_burn,
                'time_needed': updated_workout_spanish.time_needed,
                'equipment_needed': translated_data.get('equipment_needed', updated_workout_spanish.equipment_needed),
                'tag': translated_data.get('tag', updated_workout_spanish.tag),
                'benefits': translated_data.get('benefits', updated_workout_spanish.benefits),
            }

            english_workout = getattr(workout_spanish, 'workout', None)
            if english_workout:
                english_serializer = WorkoutSerializer(english_workout, data=english_data, partial=False)
                english_serializer.is_valid(raise_exception=True)
                english_serializer.save()
            else:
                english_serializer = WorkoutSerializer(data=english_data)
                english_serializer.is_valid(raise_exception=True)
                english_workout = english_serializer.save()
                english_workout.related_workout = workout_spanish
                english_workout.save()

            return Response(serializer.data)
        except Exception as e:
            return Response({"error": f"Failed to update translated workout: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Partially update a Spanish workout (Admin only)", tags=["WorkoutSpanish"])
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete a Spanish workout (Admin only)", tags=["WorkoutSpanish"])
    def destroy(self, request, *args, **kwargs):
        workout_spanish = self.get_object()
        workout_spanish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class GetEnglishWorkoutByUniqueIdView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get English workout by unique_id",
        manual_parameters=[
            openapi.Parameter('unique_id', openapi.IN_PATH, description="Unique ID of the workout", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response("Success", WorkoutSerializer),
            404: "Workout not found"
        },
        tags=["User get single workout"]
    )

    def get(self, request, unique_id):
        workout = Workout.objects.filter(unique_id=unique_id).first()
        if not workout:
            return Response({"detail": "Workout not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WorkoutSerializer(workout)
        return Response(serializer.data, status=200)
    

class GetSpanishWorkoutByUniqueIdView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Get Spanish workout by unique_id",
        manual_parameters=[
            openapi.Parameter('unique_id', openapi.IN_PATH, description="Unique ID of the workout", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response("Success", WorkoutSpanishSerializer),
            404: "Spanish workout not found"
        },
        tags=["User get single workout"]
    )
    def get(self, request, unique_id):
        workout = WorkoutSpanish.objects.filter(unique_id=unique_id).first()
        if not workout:
            return Response({"detail": "Spanish workout not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WorkoutSpanishSerializer(workout)
        return Response(serializer.data, status=200)





