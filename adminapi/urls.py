from rest_framework.routers import DefaultRouter
from django.urls import path, include
from recipe.views import RecipeAdminViewSet, RecipeSpanishAdminViewSet
from workout.views import WorkoutAdminViewSet,WorkoutSpanishAdminViewSet
from termsandpolicy.views import TermsAndConditionsViewSet, PrivacyPolicyViewSet
from subscription.views import PackageViewSet
from accounts.views import AdminDashboardStatsView,UserMonthlyStatsView,SubscriptionMonthlyStatsView
from .views import UserListView,UserDetailView,UserStatsView


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
    path('dashboard-Stats/', AdminDashboardStatsView.as_view(), name='dashboard-Stats'),
    path('user-Monthly-stats/', UserMonthlyStatsView.as_view(), name='user-daily-stats'),
    path('revenue-Monthly-stats/', SubscriptionMonthlyStatsView.as_view(), name='revenue-Monthly-stats'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('user-stats/<int:user_id>/', UserStatsView.as_view(), name='user-stats'),
]