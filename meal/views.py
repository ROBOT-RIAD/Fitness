from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta
from .serializers import DaywiseDailyMealSerializer,MealEntryWithFullRecipeSerializer,MealEntryWithFullRecipeSpanishSerializer
from .models import MealPlan, DailyMeal, MealEntry
from recipe.models import Recipe,RecipeSpanish
from accounts.models import Profile
from accounts.permissions import IsUserRole
from .services import build_meal_plan
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import time
import datetime
from django.db.models import Sum


MEAL_TYPE_TRANSLATIONS = {
    "Breakfast": "Desayuno",
    "Snack": "Merienda",
    "Snack 1": "Merienda 1",
    "Lunch": "Almuerzo",
    "Snack 2": "Merienda 2",
    "Dinner": "Cena",
    "Snack 3": "Merienda 3",
    "Post-Dinner": "Después de la cena",
    "Late Snack": "Merienda nocturna"
}



class GenerateMealPlanView(APIView):
    permission_classes = [IsAuthenticated]

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
                    recipe=recipe,  # can be None if not found
                    eating_time=datetime.datetime.strptime(m["eating_time"], "%H:%M").time() if "eating_time" in m else None
                )

        # 7. Return response
        return Response({
            "detail": "Meal plan created successfully",
            "meal_plan_id": meal_plan.id,
            "meal_plan_name": meal_plan_name,
            "tags": tags
        }, status=status.HTTP_201_CREATED)



class DaywiseMealInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(
        operation_summary="Get day-wise meal info",
        operation_description="""
        Returns daily meals for a given MealPlan (identified by `plan_id`), 
        including date, meal type, and basic recipe info (image and calories).
        """,
        tags=['All Day Wise Info Collect User Recipe'],
        responses={200: DaywiseDailyMealSerializer(many=True)}
    )

    def get(self, request, plan_id):
        try:
            meal_plan = MealPlan.objects.get(id=plan_id, user=request.user)
        except MealPlan.DoesNotExist:
            return Response({"detail": "Meal plan not found."}, status=status.HTTP_404_NOT_FOUND)
         

        meal_plan.mark_complete_if_expired()
        # Check if the meal plan is active
        if meal_plan.is_completed or meal_plan.is_cancelled:
            return Response(
                {"detail": "You have no active meal plan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if meal_plan.is_completed:
            return Response(
                {"detail": "You have no active meal plan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        daily_meals = DailyMeal.objects.filter(meal_plan=meal_plan).order_by('date')
        total_days = daily_meals.count()
        total_meals = 0
        total_calories = 0.0
        for day in daily_meals:
            for meal in day.meals.all():
                total_meals += 1
                if meal.recipe and meal.recipe.calories:
                    total_calories += float(meal.recipe.calories)


        # Fetch and return daily meals
        daily_meals = DailyMeal.objects.filter(meal_plan=meal_plan).order_by('date')
        serializer = DaywiseDailyMealSerializer(daily_meals, many=True)
        return Response({
        "status": {
            "day": total_days,
            "total_calories": round(total_calories, 2),
            "total_meals": total_meals,
            "start_date": meal_plan.start_date,
            "end_date": meal_plan.end_date,
        },
        "days": serializer.data
    })
    




class SpanishDaywiseMealInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get day-wise meal info (Spanish)",
        operation_description="""
        Returns daily meals for a given MealPlan (identified by plan_id),
        with meal_type translated to Spanish. Includes date, image, and calories.
        """,
        tags=['All Day Wise Info Collect User Recipe'],
        responses={200: DaywiseDailyMealSerializer(many=True)}
    )
    def get(self, request, plan_id):
        try:
            meal_plan = MealPlan.objects.get(id=plan_id, user=request.user)
        except MealPlan.DoesNotExist:
            return Response({"detail": "Meal plan not found."}, status=status.HTTP_404_NOT_FOUND)

        if meal_plan.is_completed or meal_plan.is_cancelled:
            return Response({"detail": "You have no active meal plan."}, status=status.HTTP_400_BAD_REQUEST)

        meal_plan.mark_complete_if_expired()
        if meal_plan.is_completed:
            return Response({"detail": "You have no active meal plan."}, status=status.HTTP_400_BAD_REQUEST)
        

        daily_meals = DailyMeal.objects.filter(meal_plan=meal_plan).order_by('date')
        total_days = daily_meals.count()
        total_meals = 0
        total_calories = 0.0
        for day in daily_meals:
            for meal in day.meals.all():
                total_meals += 1
                if meal.recipe and meal.recipe.calories:
                    total_calories += float(meal.recipe.calories)

        daily_meals = DailyMeal.objects.filter(meal_plan=meal_plan).order_by('date')
        serializer = DaywiseDailyMealSerializer(daily_meals, many=True)
        data = serializer.data

        # Predefined meal_type translation
        MEAL_TYPE_TRANSLATIONS = {
                "Breakfast": "Desayuno",
                "Snack 1": "Merienda 1",
                "Lunch": "Almuerzo",
                "Snack 2": "Merienda 2",
                "Dinner": "Cena",
                "Snack 3": "Merienda 3",
                "Post-Dinner": "Después de la cena",
                "Late Snack": "Merienda nocturna"
            }

        for day in data:
            for meal in day['meals']:
                meal_type_en = meal['meal_type']
                meal['meal_type'] = MEAL_TYPE_TRANSLATIONS.get(meal_type_en, meal_type_en)


                for day in data:
                    for meal in day['meals']:
                        meal_type_en = meal['meal_type']
                        meal['meal_type'] = MEAL_TYPE_TRANSLATIONS.get(meal_type_en, meal_type_en)

                return Response({
        "status": {
            "day": total_days,
            "total_calories": round(total_calories, 2),
            "total_meals": total_meals,
            "start_date": meal_plan.start_date,
            "end_date": meal_plan.end_date,
        },
        "days": data
    })



class DailyMealDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get meals for a specific day",
        operation_description="Returns all meals for the given DailyMeal ID, including meal_type, full recipe data, and nutritional summary.",
        manual_parameters=[
            openapi.Parameter(
                'daily_meal_id',
                openapi.IN_PATH,
                description="ID of the DailyMeal object",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        tags=['Day wise all meal list'],
        responses={
            200: openapi.Response(
                "List of meal entries with nutritional status",
                MealEntryWithFullRecipeSerializer(many=True)
            ),
            403: "Not authorized",
            404: "DailyMeal not found"
        }
    )
    def get(self, request, daily_meal_id):
        try:
            daily_meal = DailyMeal.objects.get(id=daily_meal_id)
        except DailyMeal.DoesNotExist:
            return Response({"detail": "DailyMeal not found."}, status=status.HTTP_404_NOT_FOUND)

        if daily_meal.meal_plan.user != request.user:
            return Response({"detail": "Not authorized for this meal."}, status=status.HTTP_403_FORBIDDEN)

        meal_entries = MealEntry.objects.filter(daily_meal=daily_meal).select_related('recipe')
        serializer = MealEntryWithFullRecipeSerializer(meal_entries, many=True)

        # Aggregate nutritional stats (ignoring cancelled or missing recipes)
        stats = {
            "total_protein": 0,
            "total_carbs": 0,
            "total_fat": 0
        }
        for entry in meal_entries:
            recipe = entry.recipe
            if recipe and not entry.cancelled:
                stats["total_protein"] += float(recipe.protein or 0)
                stats["total_carbs"] += float(recipe.carbs or 0)
                stats["total_fat"] += float(recipe.fat or 0)

        return Response({
            "status": stats,
            "meals": serializer.data,
        }, status=status.HTTP_200_OK)


class SpanishDailyMealDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get meals for a specific day (Spanish)",
        operation_description="Returns all meals for the given DailyMeal ID, including meal_type (translated to Spanish), full SPANISH recipe data, and nutritional summary.",
        manual_parameters=[
            openapi.Parameter(
                'daily_meal_id',
                openapi.IN_PATH,
                description="ID of the DailyMeal object",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        tags=['Day wise all meal list'],
        responses={
            200: openapi.Response(
                "List of Spanish meal entries with nutritional status",
                MealEntryWithFullRecipeSpanishSerializer(many=True)
            ),
            403: "Not authorized",
            404: "DailyMeal not found"
        }
    )
    def get(self, request, daily_meal_id):
        try:
            daily_meal = DailyMeal.objects.get(id=daily_meal_id)
        except DailyMeal.DoesNotExist:
            return Response({"detail": "DailyMeal not found."}, status=status.HTTP_404_NOT_FOUND)

        if daily_meal.meal_plan.user != request.user:
            return Response({"detail": "Not authorized for this meal."}, status=status.HTTP_403_FORBIDDEN)

        meal_entries = MealEntry.objects.filter(daily_meal=daily_meal).select_related('recipe')
        serializer = MealEntryWithFullRecipeSpanishSerializer(meal_entries, many=True)
        data = serializer.data

        # ✅ Translate meal_type to Spanish
        for meal in data:
            english_meal_type = meal.get('meal_type')
            meal['meal_type'] = MEAL_TYPE_TRANSLATIONS.get(english_meal_type, english_meal_type)

        # ✅ Calculate nutrition from RecipeSpanish
        stats = {
            "total_protein": 0.0,
            "total_carbs": 0.0,
            "total_fat": 0.0
        }

        for entry in meal_entries:
            recipe = entry.recipe
            if recipe and not entry.cancelled:
                try:
                    spanish_recipe = RecipeSpanish.objects.get(unique_id=recipe.unique_id)
                    stats["total_protein"] += float(spanish_recipe.protein or 0)
                    stats["total_carbs"] += float(spanish_recipe.carbs or 0)
                    stats["total_fat"] += float(spanish_recipe.fat or 0)
                except RecipeSpanish.DoesNotExist:
                    pass

        return Response({
            "status": {
                "total_protein": round(stats["total_protein"], 2),
                "total_carbs": round(stats["total_carbs"], 2),
                "total_fat": round(stats["total_fat"], 2),
            },
            "meals": data,
        }, status=status.HTTP_200_OK)

