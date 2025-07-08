from rest_framework.routers import DefaultRouter
from django.urls import path, include
from recipe.views import RecipeAdminViewSet
from workout.views import WorkoutAdminViewSet
from termsandpolicy.views import TermsAndConditionsViewSet, PrivacyPolicyViewSet
from subscription.views import PackageViewSet


router = DefaultRouter()

router.register('recipes', RecipeAdminViewSet, basename='admin-recipes')
router.register('workouts', WorkoutAdminViewSet, basename='admin-workouts')
router.register('terms', TermsAndConditionsViewSet, basename='terms')
router.register('privacy', PrivacyPolicyViewSet, basename='privacy')
router.register('packages', PackageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]