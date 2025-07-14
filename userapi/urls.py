from django.urls import path
from meal.views import GenerateMealPlanView

urlpatterns = [
    path("meal-plans/generate/", GenerateMealPlanView.as_view(), name="generate-meal-plan"),
]

