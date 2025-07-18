from django.urls import path
from meal.views import GenerateMealPlanView
from workoutplan.views import GenerateWorkoutPlanView
from .views import UserFullInfoAPIView,UserSpanishFullInfoAPIView
from meal.views import DaywiseMealInfoAPIView,SpanishDaywiseMealInfoAPIView,DailyMealDetailAPIView,SpanishDailyMealDetailAPIView

urlpatterns = [
    path("meal-plans/generate/", GenerateMealPlanView.as_view(), name="generate-meal-plan"),
    path("workout-plans/generate/", GenerateWorkoutPlanView.as_view(), name="generate-meal-plan"),
    path('user/info/', UserFullInfoAPIView.as_view(), name='user-full-info'),
    path('user/info/spanish/', UserSpanishFullInfoAPIView.as_view(), name='user-full-info-spanish'),
    path('meal-plan/daywise/<int:plan_id>/', DaywiseMealInfoAPIView.as_view(), name='daywise-meal-info'),
    path('spanish/meal-plan/daywise/<int:plan_id>/', SpanishDaywiseMealInfoAPIView.as_view(), name='daywise-meal-info'),
    path('meal/day/<int:daily_meal_id>/', DailyMealDetailAPIView.as_view(), name='daily-meal-detail'),    
    path('spanish/meal/day/<int:daily_meal_id>/', SpanishDailyMealDetailAPIView.as_view(), name='spanish-daily-meal-detail'),    
]

