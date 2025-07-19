from django.urls import path
from meal.views import GenerateMealPlanView
from workoutplan.views import GenerateWorkoutPlanView
from .views import UserFullInfoAPIView,UserSpanishFullInfoAPIView
from meal.views import DaywiseMealInfoAPIView,SpanishDaywiseMealInfoAPIView,DailyMealDetailAPIView,SpanishDailyMealDetailAPIView,TodaysMealAPIView,SpanishTodaysMealAPIView,UpdateMealCompletionStatusAPIView
from recipe.views import SingleRecipeDetailAPIView,SpanishSingleRecipeDetailAPIView

urlpatterns = [
    path("meal-plans/generate/", GenerateMealPlanView.as_view(), name="generate-meal-plan"),
    path("workout-plans/generate/", GenerateWorkoutPlanView.as_view(), name="generate-meal-plan"),
    path('user/info/', UserFullInfoAPIView.as_view(), name='user-full-info'),
    path('user/info/spanish/', UserSpanishFullInfoAPIView.as_view(), name='user-full-info-spanish'),
    path('meal-plan/daywise/<int:plan_id>/', DaywiseMealInfoAPIView.as_view(), name='daywise-meal-info'),
    path('spanish/meal-plan/daywise/<int:plan_id>/', SpanishDaywiseMealInfoAPIView.as_view(), name='daywise-meal-info'),
    path('meal/day/<int:daily_meal_id>/', DailyMealDetailAPIView.as_view(), name='daily-meal-detail'),    
    path('spanish/meal/day/<int:daily_meal_id>/', SpanishDailyMealDetailAPIView.as_view(), name='spanish-daily-meal-detail'),
    path('recipes/<str:unique_id>/', SingleRecipeDetailAPIView.as_view(), name='single-recipe-detail'),    
    path('spanish/recipes/<str:unique_id>/', SpanishSingleRecipeDetailAPIView.as_view(), name='spanish-single-recipe-detail'), 
    path('meals/today/', TodaysMealAPIView.as_view(), name='todays-meals'),   
    path('spanish/meals/today/', SpanishTodaysMealAPIView.as_view(), name='spanish-todays-meals'),
    path('meals/entry/complete/<int:pk>/', UpdateMealCompletionStatusAPIView.as_view(), name='update-meal-completed'),   
]

