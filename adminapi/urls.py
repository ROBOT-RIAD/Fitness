from rest_framework.routers import DefaultRouter
from django.urls import path, include
from recipe.views import RecipeAdminViewSet
from workout.views import WorkoutAdminViewSet

router = DefaultRouter()
router.register('recipes', RecipeAdminViewSet, basename='admin-recipes')
router.register('workouts', WorkoutAdminViewSet, basename='admin-workouts')
urlpatterns = [
    path('', include(router.urls)),
]