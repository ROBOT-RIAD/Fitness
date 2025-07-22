# views.py
from datetime import date
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg import openapi
from meal.models import DailyMeal
from workoutplan.models import DailyWorkout
from .serializers import DailyMealTodaySerializer, DailyWorkoutTodaySerializer,AIRecommendedDataSerializer
from datetime import date, datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from AiChat.models import HealthProfile


class TodayDailyDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get DailyMeal & DailyWorkout by date (default: today)",
        tags=["home"],
        manual_parameters=[
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Optional date (format: YYYY-MM-DD). Defaults to today.",
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def get(self, request):
        user = request.user

        # Get date from query params or fallback to today
        date_str = request.query_params.get('date')
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        daily_meal = DailyMeal.objects.filter(
            meal_plan__user=user,
            date=target_date
        ).first()

        daily_workout = DailyWorkout.objects.filter(
            workout_plan__user=user,
            date=target_date
        ).first()

        try:
            profile = request.user.health_profile
        except HealthProfile.DoesNotExist:
            return Response({"detail": "Health profile not found."}, status=404)
        serializer = AIRecommendedDataSerializer(profile)
        return Response({
            "date": target_date,
            "daily_meal": DailyMealTodaySerializer(daily_meal).data if daily_meal else None,
            "daily_workout": DailyWorkoutTodaySerializer(daily_workout).data if daily_workout else None,
            "AiRecomended":serializer.data,
        })

