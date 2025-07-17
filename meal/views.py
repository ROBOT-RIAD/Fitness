from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta

from .models import MealPlan, DailyMeal, MealEntry
from recipe.models import Recipe
from accounts.models import Profile
from accounts.permissions import IsUserRole
from .services import build_meal_plan

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GenerateMealPlanView(APIView):
    permission_classes = [IsAuthenticated,IsUserRole]

    @swagger_auto_schema(
        operation_summary="Generate a 15-Day AI-Powered Meal Plan",
        operation_description="""
        Generates a personalized 15-day meal plan based on the authenticated user's profile and available recipes.
        This uses OpenAI to intelligently create meal suggestions (breakfast, lunch, dinner) for each day.

        ✅ No request body is required. Only the logged-in user's profile is used.
        """,
        tags=["AI Meal Plan"],
        responses={
            201: openapi.Response(
                description="Meal plan created successfully",
                examples={
                    "application/json": {
                        "detail": "Meal plan created successfully",
                        "meal_plan_id": 42,
                        "meal_plan_name": "High Protein Muscle Gain Plan",
                        "tags": "protein,balanced,fitness"
                    }
                }
            ),
            404: openapi.Response(description="User profile not found"),
            500: openapi.Response(description="OpenAI error or internal failure")
        }
    )

    def post(self, request):
        user = request.user

        # 1. Ensure user has profile
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=404)

        # 2. Get recipes
        recipes_qs = Recipe.objects.exclude(unique_id__isnull=True).exclude(unique_id__exact='')

        # 3. Generate AI meal plan
        try:
            result = build_meal_plan(profile, recipes_qs, days=15)
            meal_plan_name = result.get("meal_plan_name", "15-Day AI Plan")
            tags = result.get("tags", "")
            plan_days = result.get("days", [])
        except Exception as e:
            return Response({"detail": f"OpenAI error: {str(e)}"}, status=500)

        # 4. Create MealPlan instance
        today = date.today()
        meal_plan = MealPlan.objects.create(
            user=user,
            meal_plan_name=meal_plan_name,
            tags=tags,
            start_date=today,
            end_date=today + timedelta(days=14),
        )

        # 5. Cache recipes by unique_id for fast lookup
        uid_cache = {r.unique_id: r for r in recipes_qs}

        # 6. Loop through days and meals
        for day in plan_days:
            daily = DailyMeal.objects.create(
                meal_plan=meal_plan,
                date=day["date"]
            )
            for m in day["meals"]:
                recipe = uid_cache.get(m["recipe_uid"])
                MealEntry.objects.create(
                    daily_meal=daily,
                    meal_type=m["meal_type"],
                    recipe=recipe  # can be None if not found
                )

        # 7. Return response
        return Response({
            "detail": "Meal plan created successfully",
            "meal_plan_id": meal_plan.id,
            "meal_plan_name": meal_plan_name,
            "tags": tags
        }, status=status.HTTP_201_CREATED)


