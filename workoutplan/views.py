from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta

from .models import WorkoutPlan, DailyWorkout, WorkoutEntry
from workout.models import Workout
from accounts.models import Profile
from accounts.permissions import IsUserRole
from .serializers import TrainingDataSerializer
from .services import build_workout_plan

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GenerateWorkoutPlanView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=TrainingDataSerializer,
        operation_summary="Generate a 15-Day AI-Powered Workout Plan",
        operation_description="""
        Generates a personalized 15-day workout plan using OpenAI based on the authenticated user's profile,
        training preferences, and available workouts.

        🔐 Requires authentication  
        🧠 Uses OpenAI (GPT-4)  
        📌 Saves full plan to database
        """,
        tags=["AI Workout Plan"],
        responses={
            201: openapi.Response(
                description="Workout plan created successfully",
                examples={
                    "application/json": {
                        "detail": "Workout plan created successfully",
                        "workout_plan_id": 101,
                        "workout_plan_name": "Lean Strength Plan",
                        "tags": "strength,endurance,home"
                    }
                }
            ),
            400: openapi.Response(description="Invalid training data"),
            404: openapi.Response(description="User profile not found"),
            500: openapi.Response(description="OpenAI error or internal failure")
        }
    )
    def post(self, request):
        user = request.user

        # 1. Validate user profile
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=404)

        # 2. Validate training input
        serializer = TrainingDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        training_data = serializer.validated_data

        # 3. Get all valid workouts
        workouts_qs = Workout.objects.exclude(unique_id__isnull=True).exclude(unique_id__exact="")

        # 4. Call OpenAI to build the plan
        try:
            result = build_workout_plan(profile, training_data, workouts_qs, days=15)
            workout_plan_name = result.get("workout_plan_name", "15-Day AI Plan")
            tags = result.get("tags", "")
            plan_days = result.get("days", [])
        except Exception as e:
            return Response({"detail": f"OpenAI error: {str(e)}"}, status=500)

        # 5. Create WorkoutPlan instance
        today = date.today()
        workout_plan = WorkoutPlan.objects.create(
            user=user,
            workout_plan_name=workout_plan_name,
            tags=tags,
            start_date=today,
            end_date=today + timedelta(days=14),
        )

        # 6. Cache workouts for quick lookup
        uid_cache = {w.unique_id: w for w in workouts_qs}

        # 7. Create DailyWorkout and WorkoutEntry entries
        for day in plan_days:
            daily = DailyWorkout.objects.create(
                workout_plan=workout_plan,
                date=day["date"],
                title=day.get("title", f"Workout - {day['date']}"),
                title_spanish=day.get("title_spanish", day.get("title", "")),
                tags=day.get("tags", tags),
                tags_spanish=day.get("tags_spanish", day.get("tags", "")),
            )
            for w in day.get("workouts", []):
                workout = uid_cache.get(w["workout_uid"])
                WorkoutEntry.objects.create(
                    daily_workout=daily,
                    workout=workout,
                    completed=False,
                    set_of=w.get("set_of", 1),
                    reps=w.get("reps", 10)
                )


        # 8. Return response
        return Response({
            "detail": "Workout plan created successfully",
            "workout_plan_id": workout_plan.id,
            "workout_plan_name": workout_plan_name,
            "tags": tags
        }, status=status.HTTP_201_CREATED)
