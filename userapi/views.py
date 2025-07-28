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
from subscription.decorators import subscription_required


class UserFullInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Apply the decorator to all view methods
    #     for method_name in ['get', 'post', 'put', 'delete']:
    #         if hasattr(self, method_name):
    #             method = getattr(self, method_name)
    #             setattr(self, method_name, subscription_required(method))


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

        if not meal_plans_qs.exists():
            # Query for the most recent completed meal plan
            recent_completed_meal_plan = MealPlan.objects.filter(user=user, is_completed=True, is_cancelled=False).order_by('-end_date').first()
            meal_plan_data = {
                "id": recent_completed_meal_plan.id if recent_completed_meal_plan else None,
                "meal_plan_name": recent_completed_meal_plan.meal_plan_name if recent_completed_meal_plan else None,
                "tags": recent_completed_meal_plan.tags if recent_completed_meal_plan else None,
                "start_date": recent_completed_meal_plan.start_date if recent_completed_meal_plan else None,
                "end_date": recent_completed_meal_plan.end_date if recent_completed_meal_plan else None,
                "is_completed": recent_completed_meal_plan.is_completed if recent_completed_meal_plan else None,
                "is_cancelled": recent_completed_meal_plan.is_cancelled if recent_completed_meal_plan else None,
            }
        else:
            meal_plan_data = MealPlanInfoSerializer(meal_plans_qs, many=True).data

        # Check if there are no active workout plans
        if not workout_plans_qs.exists():
            # Query for the most recent completed workout plan
            recent_completed_workout_plan = WorkoutPlan.objects.filter(user=user, is_completed=True, is_cancelled=False).order_by('-end_date').first()
            workout_plan_data = {
                "id": recent_completed_workout_plan.id if recent_completed_workout_plan else None,
                "workout_plan_name": recent_completed_workout_plan.workout_plan_name if recent_completed_workout_plan else None,
                "tags": recent_completed_workout_plan.tags if recent_completed_workout_plan else None,
                "start_date": recent_completed_workout_plan.start_date if recent_completed_workout_plan else None,
                "end_date": recent_completed_workout_plan.end_date if recent_completed_workout_plan else None,
                "is_completed": recent_completed_workout_plan.is_completed if recent_completed_workout_plan else None,
                "is_cancelled": recent_completed_workout_plan.is_cancelled if recent_completed_workout_plan else None,
            }
        else:
            workout_plan_data = WorkoutPlanInfoSerializer(workout_plans_qs, many=True).data

        return Response({
            "profile": profile_data,
            "meal_plans": meal_plan_data,
            "workout_plans": workout_plan_data,
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

        if not meal_plans_qs.exists():
            # Query for the most recent completed meal plan
            recent_completed_meal_plan = MealPlan.objects.filter(user=user, is_completed=True, is_cancelled=False).order_by('-end_date').first()
            meal_plan_data = {
                "id": recent_completed_meal_plan.id if recent_completed_meal_plan else None,
                "meal_plan_name": recent_completed_meal_plan.meal_plan_name if recent_completed_meal_plan else None,
                "tags": recent_completed_meal_plan.tags if recent_completed_meal_plan else None,
                "start_date": recent_completed_meal_plan.start_date if recent_completed_meal_plan else None,
                "end_date": recent_completed_meal_plan.end_date if recent_completed_meal_plan else None,
                "is_completed": recent_completed_meal_plan.is_completed if recent_completed_meal_plan else None,
                "is_cancelled": recent_completed_meal_plan.is_cancelled if recent_completed_meal_plan else None,
            }
        else:
            meal_plan_data = MealPlanInfoSerializer(meal_plans_qs, many=True).data

        # Check if there are no active workout plans
        if not workout_plans_qs.exists():
            # Query for the most recent completed workout plan
            recent_completed_workout_plan = WorkoutPlan.objects.filter(user=user, is_completed=True, is_cancelled=False).order_by('-end_date').first()
            workout_plan_data = {
                "id": recent_completed_workout_plan.id if recent_completed_workout_plan else None,
                "workout_plan_name": recent_completed_workout_plan.workout_plan_name if recent_completed_workout_plan else None,
                "tags": recent_completed_workout_plan.tags if recent_completed_workout_plan else None,
                "start_date": recent_completed_workout_plan.start_date if recent_completed_workout_plan else None,
                "end_date": recent_completed_workout_plan.end_date if recent_completed_workout_plan else None,
                "is_completed": recent_completed_workout_plan.is_completed if recent_completed_workout_plan else None,
                "is_cancelled": recent_completed_workout_plan.is_cancelled if recent_completed_workout_plan else None,
            }
        else:
            workout_plan_data = WorkoutPlanInfoSerializer(workout_plans_qs, many=True).data
 
        data = {
            "profile": profile_data,
            "meal_plans": meal_plan_data,
            "workout_plans": workout_plan_data,
        }

        translated_data = translate_to_spanish(data)
        return Response(translated_data)




