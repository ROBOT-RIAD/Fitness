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

class UserPagination(PageNumberPagination):
    page_size = 10  # Number of users per page
    page_size_query_param = 'page_size'  # Optional query param to customize page size
    max_page_size = 100  # Max page size that can be requested

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
        # Step 1: Check if the user exists
        try:
            # Fetch the user by the given user_id
            user = User.objects.get(id=user_id)
            
            # Step 2: Fetch completed workout plan and meal plan
            recent_workout_plan = None
            recent_meal_plan = None

            # Check if the user has a completed workout plan
            if user.workout_plans.filter(is_completed=True).exists():
                recent_workout_plan = user.workout_plans.filter(is_completed=True).order_by('-end_date').first()
            
            # Check if the user has a completed meal plan
            if user.meal_plans.filter(is_completed=True).exists():
                recent_meal_plan = user.meal_plans.filter(is_completed=True).order_by('-end_date').first()

            # Step 3: Get the total number of completed meal and workout entries
            total_completed_meal_entries = MealEntry.objects.filter(daily_meal__meal_plan__user=user, completed=True).count()
            total_completed_workout_entries = WorkoutEntry.objects.filter(daily_workout__workout_plan__user=user, completed=True).count()

            #Achievement
            achievement = AchievementSerializer(user)

            # Step 4: Prepare the response data
            data = {
                "achievement":achievement,
                "recent_workout_plan": recent_workout_plan.workout_plan_name if recent_workout_plan else "No completed plan",
                "recent_meal_plan": recent_meal_plan.meal_plan_name if recent_meal_plan else "No completed plan",
                "total_completed_meal_entries": total_completed_meal_entries,
                "total_completed_workout_entries": total_completed_workout_entries,
            }

            return Response(data, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)




