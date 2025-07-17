from django.urls import path
from meal.views import GenerateMealPlanView
from workoutplan.views import GenerateWorkoutPlanView
from .views import UserFullInfoAPIView,UserSpanishFullInfoAPIView

urlpatterns = [
    path("meal-plans/generate/", GenerateMealPlanView.as_view(), name="generate-meal-plan"),
    path("workout-plans/generate/", GenerateWorkoutPlanView.as_view(), name="generate-meal-plan"),
    path('user/info/', UserFullInfoAPIView.as_view(), name='user-full-info'),
    path('user/info/spanish/', UserSpanishFullInfoAPIView.as_view(), name='user-full-info-spanish'),
]

