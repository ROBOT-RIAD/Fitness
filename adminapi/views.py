from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from .serializers import UserSerializer,SingleUserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from meal.models import MealPlan,MealEntry
from workoutplan.models import WorkoutPlan,WorkoutEntry
from completeinfo.serializers import AchievementSerializer
from completeinfo.models import FitnessProfile


class UserPagination(PageNumberPagination):
    page_size = 5  # Number of users per page
    page_size_query_param = 'page_size'  # Optional query param to customize page size




class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["admin"])
    def get(self, request):
        
        ordering_field = 'date_joined' 
        ordering_direction = request.query_params.get('ordering_direction', 'asc')
        
        if ordering_direction == 'desc':
            ordering_field = f'-{ordering_field}'  

        fullname_query = request.query_params.get('fullname', None)
        if fullname_query:
            users = User.objects.filter(profile__fullname__icontains=fullname_query)
        else:
            users = User.objects.all()

        users = users.exclude(is_staff=True, is_superuser=True)
        users = users.exclude(role='admin')

        package_name_query = request.query_params.get('package_name', None)
        if package_name_query:
            users = users.filter(subscriptions__package_name__icontains=package_name_query) 

        users = users.prefetch_related(
            'subscriptions',
            'profile'
        ).order_by(ordering_field)

        paginator = UserPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True,context ={'request':request})
        return paginator.get_paginated_response(serializer.data)





class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(tags=["admin"])
    def get(self, request, user_id):
        try:
            # Fetch user by ID
            user = User.objects.get(id=user_id)
            
            # Serialize the user data
            serializer = SingleUserSerializer(user)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)




class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(tags=["admin"])

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            recent_workout_plan = None
            recent_meal_plan = None
            AI_weight = 0
            recent_fitness_profile = user.fitness_profiles.order_by('-created_at').first()
            if recent_fitness_profile:
                AI_weight = recent_fitness_profile.current_weight
            
            health = getattr(user, 'health_profile', None)
            if health :
                AI_weight = health.perfect_weight_kg

            # total_weight_difarent = user.profile.weight - AI_weight
            user_weight = user.profile.weight if user.profile.weight is not None else 0
            total_weight_difarent = user_weight - AI_weight

            if user.workout_plans.filter(is_completed=True).exists():
                recent_workout_plan = user.workout_plans.filter(is_completed=True).order_by('-end_date').first()
            
            if user.meal_plans.filter(is_completed=True).exists():
                recent_meal_plan = user.meal_plans.filter(is_completed=True).order_by('-end_date').first()

            total_completed_meal_entries = MealEntry.objects.filter(daily_meal__meal_plan__user=user, completed=True).count()
            total_meal_entries = MealEntry.objects.filter(daily_meal__meal_plan__user=user).count()

            total_completed_workout_entries = WorkoutEntry.objects.filter(daily_workout__workout_plan__user=user, completed=True).count()
            total_workout_entries = WorkoutEntry.objects.filter(daily_workout__workout_plan__user=user).count()

            # Check if user has an achievement related object
            achievement = user.achievement if hasattr(user, 'achievement') and user.achievement is not None else None

            # If achievement exists, serialize it
            if achievement:
                achievement_data = AchievementSerializer(achievement).data
            else:
                achievement_data = {}

            fitness_profiles = FitnessProfile.objects.filter(user=user)
            weights_list = [profile.current_weight for profile in fitness_profiles]
            
            # Set default value for weight_change if achievement is None
            value = 0
            if achievement:
                print(achievement_data.get('weight_change', 0))
                value = float(achievement_data.get('weight_change', 0))
            
            progress = 0
            if value == 0:
                progress = 0
            else:
                progress = (value / total_weight_difarent) * 100

            data = {
                "progress": int(progress),
                "AI_weight": AI_weight,
                "curent_weight": user.profile.weight,
                "recent_workout_plan": recent_workout_plan.workout_plan_name if recent_workout_plan else "No completed plan",
                "recent_meal_plan": recent_meal_plan.meal_plan_name if recent_meal_plan else "No completed plan",
                "total_meal_entries": total_meal_entries,
                "total_completed_meal_entries": total_completed_meal_entries,
                "total_workout_entries": total_workout_entries,
                "total_completed_workout_entries": total_completed_workout_entries,
                'achievement': achievement_data,
                "weights_list": weights_list,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



