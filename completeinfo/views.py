from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from meal.models import MealPlan
from workoutplan.models import WorkoutPlan
from .models import FitnessProfile
from .serializers import FitnessProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class FitnessProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new FitnessProfile",
        operation_description=( 
            "Create a FitnessProfile for the authenticated user. At least one of `meal_plan_id` or `workout_plan_id` "
            "must be provided. Either a `meal_plan_id` or `workout_plan_id` will be assigned to the created FitnessProfile."
        ),
        request_body=FitnessProfileSerializer,
        tags=["Fitness profile"],
        responses={
            201: openapi.Response(description="Fitness Profile created successfully", schema=FitnessProfileSerializer),
            400: openapi.Response(description="Bad Request, at least one of `meal_plan_id` or `workout_plan_id` must be provided"),
            404: openapi.Response(description="Not Found, if MealPlan or WorkoutPlan does not exist"),
        },
        manual_parameters=[
            openapi.Parameter('meal_plan_id', openapi.IN_FORM, description="ID of the MealPlan (optional)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('workout_plan_id', openapi.IN_FORM, description="ID of the WorkoutPlan (optional)", type=openapi.TYPE_INTEGER),
        ]
    )
    def post(self, request, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        # Get optional meal_plan_id and workout_plan_id from the request data
        meal_plan_id = request.data.get('meal_plan')
        workout_plan_id = request.data.get('workout_plan')

        # Validate if at least one of meal_plan_id or workout_plan_id is provided
        if not meal_plan_id and not workout_plan_id:
            return Response({"error": "At least one of 'meal_plan_id' or 'workout_plan_id' must be provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Handle meal_plan and workout_plan if provided
        meal_plan = None
        workout_plan = None

        # Fetch MealPlan if provided
        if meal_plan_id:
            try:
                meal_plan = MealPlan.objects.get(id=meal_plan_id)
            except MealPlan.DoesNotExist:
                return Response({"error": f"MealPlan with ID {meal_plan_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

        # Fetch WorkoutPlan if provided
        if workout_plan_id:
            try:
                workout_plan = WorkoutPlan.objects.get(id=workout_plan_id)
            except WorkoutPlan.DoesNotExist:
                return Response({"error": f"WorkoutPlan with ID {workout_plan_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user has already submitted a profile with the same meal_plan and workout_plan
        existing_profile = FitnessProfile.objects.filter(
            user=user,
            meal_plan=meal_plan,
            workout_plan=workout_plan
        ).exists()

        if existing_profile:
            return Response(
                {"error": "You have already submitted a fitness profile with the same MealPlan and WorkoutPlan."},
                status=status.HTTP_409_CONFLICT
            )
        
        # Prepare the data to be passed into the serializer
        data = {
            'user': user.id,
            'current_weight': request.data.get('current_weight'),
            'abdominal': request.data.get('abdominal'),
            'sacroiliac': request.data.get('sacroiliac'),
            'subscapularis': request.data.get('subscapularis'),
            'triceps': request.data.get('triceps'),
            'feeling': request.data.get('feeling'),
            'total_meal': request.data.get('total_meal'),
            'workout_consistency': request.data.get('workout_consistency'),
            'energy_level': request.data.get('energy_level'),
            'injuries_pain': request.data.get('injuries_pain'),
            'meal_plan': meal_plan.id if meal_plan else None,
            'workout_plan': workout_plan.id if workout_plan else None,
        }

        # Validate and serialize the data
        serializer = FitnessProfileSerializer(data=data)
        if serializer.is_valid():
            # Save the FitnessProfile instance
            serializer.save(user=user, meal_plan=meal_plan, workout_plan=workout_plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
