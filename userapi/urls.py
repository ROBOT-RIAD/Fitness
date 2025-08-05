
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from meal.views import GenerateMealPlanView
from workoutplan.views import GenerateWorkoutPlanView,ActiveWorkoutPlanView,CompleteTodayWorkoutView,DailyWorkoutDetailsView,SpanishDailyWorkoutDetailsView,TodayWorkoutView,SpanishWorkoutEntryListView,UpdateTodayWorkoutEntryAPIView
from .views import UserFullInfoAPIView,UserSpanishFullInfoAPIView
from meal.views import DaywiseMealInfoAPIView,SpanishDaywiseMealInfoAPIView,DailyMealDetailAPIView,SpanishDailyMealDetailAPIView,TodaysMealAPIView,SpanishTodaysMealAPIView,UpdateMealCompletionStatusAPIView
from recipe.views import SingleRecipeDetailAPIView,SpanishSingleRecipeDetailAPIView,RecipeListView,SpanishRecipeListView
from workout.views import GetEnglishWorkoutByUniqueIdView, GetSpanishWorkoutByUniqueIdView,WorkoutListAPIView,SpanishWorkoutListAPIView
from home.views import TodayDailyDetailsAPIView,SpanishTodayDailyDetailsAPIView
from accounts.views import DeleteUserView
from completeinfo.views import FitnessProfileCreateView,UserAchievementDetailView,Aifeedback

router = DefaultRouter()


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
    path('active-workout-plan/', ActiveWorkoutPlanView.as_view(), name='active-workout-plan'),
    path('complete-today/', CompleteTodayWorkoutView.as_view(), name='complete-today-workout'),   
    path('daily-workout/details/<int:pk>/', DailyWorkoutDetailsView.as_view(), name='daily-workout-details'),
    path('spanish-daily-workout/details/<int:pk>/', SpanishDailyWorkoutDetailsView.as_view(), name='spanish-daily-workout-details'),
    path('workout/<str:unique_id>/', GetEnglishWorkoutByUniqueIdView.as_view(), name='get-english-workout'),
    path('spanish/workout/<str:unique_id>/', GetSpanishWorkoutByUniqueIdView.as_view(), name='get-spanish-workout'),
    path('workouts/today/', TodayWorkoutView.as_view(), name='today-workouts'),
    path('spanish-workouts/today/', SpanishWorkoutEntryListView.as_view(), name='spanish-today-workouts'),
    path('workout/update-today-entry/<int:pk>/',UpdateTodayWorkoutEntryAPIView.as_view(),name='update-today-workout-entry'),
    path('plans/today/', TodayDailyDetailsAPIView.as_view(), name='today-plans'),
    path('spanish/plans/today/', SpanishTodayDailyDetailsAPIView.as_view(), name='today-plans'),
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('spanish/recipes/', SpanishRecipeListView.as_view(), name='spanish-recipe-list'),
    path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete-account'),
    path('create/', FitnessProfileCreateView.as_view(), name='create_fitness_profile'),
    path('achievement/details/', UserAchievementDetailView.as_view(), name='user-achievement-details'),
    path('all/workouts/', WorkoutListAPIView.as_view(), name='workout-list'),
    path('all/spanish/workouts/', SpanishWorkoutListAPIView.as_view(), name='spanish-workout-list'),
    path('user/feedback/', Aifeedback.as_view(), name='user-feedback'),
    path('', include(router.urls)),
]

