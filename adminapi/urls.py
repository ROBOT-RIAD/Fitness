from rest_framework.routers import DefaultRouter
from django.urls import path, include
from recipe.views import RecipeAdminViewSet, RecipeSpanishAdminViewSet
from workout.views import WorkoutAdminViewSet,WorkoutSpanishAdminViewSet
from termsandpolicy.views import TermsAndConditionsViewSet, PrivacyPolicyViewSet
from subscription.views import PackageViewSet


router = DefaultRouter()


router.register('workouts', WorkoutAdminViewSet, basename='admin-workouts')
router.register('terms', TermsAndConditionsViewSet, basename='terms')
router.register('privacy', PrivacyPolicyViewSet, basename='privacy')
router.register('packages', PackageViewSet)
router.register(r'recipes', RecipeAdminViewSet, basename='recipe')
router.register(r'recipes-spanish', RecipeSpanishAdminViewSet, basename='recipe-spanish')
router.register(r'workouts-spanish', WorkoutSpanishAdminViewSet, basename='workouts-spanish')

urlpatterns = [
    path('', include(router.urls)),
]