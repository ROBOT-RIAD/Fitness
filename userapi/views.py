from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile
from meal.models import MealPlan
from workoutplan.models import WorkoutPlan
from .serializers import ProfileInfoSerializer, MealPlanInfoSerializer, WorkoutPlanInfoSerializer
from .services import translate_to_spanish
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserFullInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get active user info (English)",
        operation_description=(
            "Returns the profile plus **active** meal & workout plans for the authenticated user. "
            "A plan is *active* if **is_completed = False** and **is_cancelled = False**."
        ),
        tags=['info'],
        responses={200: openapi.Response(description="English user profile with active plans")}
    )
    def get(self, request):
        user = request.user

        profile = Profile.objects.filter(user=user).first()
        profile_data = ProfileInfoSerializer(profile).data if profile else None

        meal_plans_qs = MealPlan.objects.filter(user=user, is_completed=False, is_cancelled=False)
        workout_plans_qs = WorkoutPlan.objects.filter(user=user, is_completed=False, is_cancelled=False)

        return Response({
            "profile": profile_data,
            "meal_plans": MealPlanInfoSerializer(meal_plans_qs, many=True).data,
            "workout_plans": WorkoutPlanInfoSerializer(workout_plans_qs, many=True).data,
        })



class UserSpanishFullInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get active user info (Spanish)",
        operation_description="Returns the translated profile and plans in Spanish.",
        tags=['info'],
        responses={200: openapi.Response(description="Spanish user profile with active plans")}
    )
    def get(self, request):
        user = request.user

        profile = Profile.objects.filter(user=user).first()
        profile_data = ProfileInfoSerializer(profile).data if profile else None

        meal_plans_qs = MealPlan.objects.filter(user=user, is_completed=False, is_cancelled=False)
        workout_plans_qs = WorkoutPlan.objects.filter(user=user, is_completed=False, is_cancelled=False)

        data = {
            "profile": profile_data,
            "meal_plans": MealPlanInfoSerializer(meal_plans_qs, many=True).data,
            "workout_plans": WorkoutPlanInfoSerializer(workout_plans_qs, many=True).data,
        }

        translated_data = translate_to_spanish(data)
        return Response(translated_data)




