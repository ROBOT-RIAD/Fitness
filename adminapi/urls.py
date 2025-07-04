from rest_framework.routers import DefaultRouter
from django.urls import path, include
from recipe.views import RecipeAdminViewSet

router = DefaultRouter()
router.register('recipes', RecipeAdminViewSet, basename='admin-recipes')

urlpatterns = [
    path('', include(router.urls)),
]