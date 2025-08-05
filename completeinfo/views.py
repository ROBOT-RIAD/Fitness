from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from meal.models import MealPlan,DailyMeal
from workoutplan.models import WorkoutPlan,DailyWorkout
from .models import FitnessProfile,Achievement
from .serializers import FitnessProfileSerializer,UserAchievementSerializer,AchievementSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.models import Profile
from accounts.models import User
from django.db.models import Max
import openai
from django.conf import settings




class FitnessProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new FitnessProfile",
        operation_description=( 
            "Create a FitnessProfile for the authenticated user. At least one of `meal_plan_id` or `workout_plan_id` "
            "must be provided. Either a `meal_plan_id` or `workout_plan_id` will be assigned to the created FitnessProfile."
        ),
        request_body=FitnessProfileSerializer,
        tags=["Fitness profile"],
        responses={
            201: openapi.Response(description="Fitness Profile created successfully", schema=FitnessProfileSerializer),
            400: openapi.Response(description="Bad Request, at least one of `meal_plan_id` or `workout_plan_id` must be provided"),
            404: openapi.Response(description="Not Found, if MealPlan or WorkoutPlan does not exist"),
        },
    )
    def post(self, request, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        # Get optional meal_plan_id and workout_plan_id from the request data
        meal_plan_id = request.data.get('meal_plan')
        workout_plan_id = request.data.get('workout_plan')

        # Validate if at least one of meal_plan_id or workout_plan_id is provided
        if not meal_plan_id and not workout_plan_id:
            return Response({"error": "At least one of 'meal_plan_id' or 'workout_plan_id' must be provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Handle meal_plan and workout_plan if provided
        meal_plan = None
        workout_plan = None

        # Fetch MealPlan if provided
        if meal_plan_id:
            try:
                meal_plan = MealPlan.objects.get(id=meal_plan_id)
            except MealPlan.DoesNotExist:
                return Response({"error": f"MealPlan with ID {meal_plan_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)

        # Fetch WorkoutPlan if provided
        if workout_plan_id:
            try:
                workout_plan = WorkoutPlan.objects.get(id=workout_plan_id)
            except WorkoutPlan.DoesNotExist:
                return Response({"error": f"WorkoutPlan with ID {workout_plan_id} does not exist."},
                                status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user has already submitted a profile with the same meal_plan and workout_plan
        existing_profile = FitnessProfile.objects.filter(
            user=user,
            meal_plan=meal_plan,
            workout_plan=workout_plan
        ).exists()

        if existing_profile:
            return Response(
                {"error": "You have already submitted a fitness profile with the same MealPlan and WorkoutPlan."},
                status=status.HTTP_409_CONFLICT
            )
        
        # Get Profile data
        profile = user.profile
        profile_weight = float(profile.weight if profile.weight is not None else 0)
        profile_abdominal = float(profile.abdominal if profile.abdominal is not None else 0)
        profile_sacroiliac = float(profile.sacroiliac if profile.sacroiliac is not None else 0)
        profile_subscapularis = float(profile.subscapularis if profile.subscapularis is not None else 0)
        profile_triceps = float(profile.triceps if profile.triceps is not None else 0)
        

        # Extract incoming data
        request_weight = float(request.data.get('current_weight'))
        request_abdominal = float(request.data.get('abdominal'))
        request_sacroiliac = float(request.data.get('sacroiliac'))
        request_subscapularis = float(request.data.get('subscapularis'))
        request_triceps = float(request.data.get('triceps'))

        weight_change = request_weight - profile_weight
        abdominal_change = ((request_abdominal - profile_abdominal)/profile_abdominal)*100
        sacrolic_change =  ((request_sacroiliac - profile_sacroiliac)/profile_sacroiliac)*100
        subscapularis_change = ((request_subscapularis - profile_subscapularis)/profile_subscapularis)*100
        triceps_change = ((request_triceps - profile_triceps)/profile_triceps)*100

        weight_increase = True if request_weight >= profile_weight else False
        abdominal_increase =True if request_abdominal >= profile_abdominal else False
        sacrolic_increase = True if request_sacroiliac >= profile_sacroiliac else False
        subscapularis_increase = True if request_subscapularis >= profile_subscapularis else False
        triceps_increase = True if request_triceps >= profile_triceps else False
        
        # Prepare the data to be passed into the serializer
        data = {
            'user': user.id,
            'current_weight': request.data.get('current_weight'),
            'abdominal': request.data.get('abdominal'),
            'sacroiliac': request.data.get('sacroiliac'),
            'subscapularis': request.data.get('subscapularis'),
            'triceps': request.data.get('triceps'),
            'feeling': request.data.get('feeling'),
            'total_meal': request.data.get('total_meal'),
            'workout_consistency': request.data.get('workout_consistency'),
            'energy_level': request.data.get('energy_level'),
            'injuries_pain': request.data.get('injuries_pain'),
            'meal_plan': meal_plan.id if meal_plan else None,
            'workout_plan': workout_plan.id if workout_plan else None,
        }
        print(data)

        # Validate and serialize the data
        serializer = FitnessProfileSerializer(data=data)
        if serializer.is_valid():
            # Save the FitnessProfile instance
            serializer.save(user=user, meal_plan=meal_plan, workout_plan=workout_plan)
           
            achievement, created = Achievement.objects.update_or_create(
                    user=user,
                    defaults={
                        'weight_change': weight_change,
                        'abdominal_change': int(abdominal_change),
                        'sacrolic_change': int(sacrolic_change),
                        'subscapularis_change': int(subscapularis_change),
                        'triceps_change': int(triceps_change),
                        'weight_increase': weight_increase,
                        'abdominal_increase': abdominal_increase,
                        'sacrolic_increase': sacrolic_increase,
                        'subscapularis_increase': subscapularis_increase,
                        'triceps_increase': triceps_increase
                    }
                )
            achievement.save()

            profile.weight = request_weight
            profile.abdominal = request_abdominal
            profile.sacroiliac = request_sacroiliac
            profile.subscapularis = request_subscapularis
            profile.triceps = request_triceps
            profile.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserAchievementDetailView(APIView):    
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get user achievement, latest meal plan, and latest workout plan",
        operation_description="Fetch the authenticated user's achievement details, the latest completed meal plan, and the latest completed workout plan, including their progress.",
        responses={
            200: openapi.Response(
                description="Successfully fetched achievement and plans",
                schema=UserAchievementSerializer,
            ),
            404: openapi.Response(
                description="Not Found: No achievement or plans found for the user",
                examples={"application/json": {"detail": "Not found."}},
            ),
            400: openapi.Response(
                description="Bad Request: Invalid or incomplete request",
                examples={"application/json": {"detail": "Invalid request."}},
            ),
        },
        tags=["User Achievement"]
    )
    def get(self, request, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        # Get the latest completed MealPlan
        latest_meal_plan = MealPlan.objects.filter(user=user, is_completed=True).order_by('-end_date').first()

        # Get the latest completed WorkoutPlan
        latest_workout_plan = WorkoutPlan.objects.filter(user=user, is_completed=True).order_by('-end_date').first()

        # Get the Achievement of the user
        achievement = Achievement.objects.filter(user=user).first()

        # Count total completed workout days for the latest workout plan
        total_completed_workout_days = DailyWorkout.objects.filter(
            workout_plan=latest_workout_plan, completed=True
        ).count() if latest_workout_plan else 0

        # Count total completed meal days for the latest meal plan
        total_completed_meal_days = DailyMeal.objects.filter(
            meal_plan=latest_meal_plan
        ).filter(
            meals__completed=True
        ).distinct().count() if latest_meal_plan else 0

        fitness_profiles = FitnessProfile.objects.filter(user=user)
        weights_list = [profile.current_weight for profile in fitness_profiles]

        # Prepare the data to send in response
        data = {
            'achievement': achievement,
            'latest_meal_plan': latest_meal_plan,
            'latest_workout_plan': latest_workout_plan,
            'total_completed_workout_days': total_completed_workout_days,
            'total_completed_meal_days': total_completed_meal_days,
        }
        print(total_completed_workout_days,total_completed_meal_days)

        # Serialize the response
        serializer = UserAchievementSerializer(user, context={'request': request})

        return Response({
            'info':serializer.data,
            'total_completed_workout_days': total_completed_workout_days,
            'total_completed_meal_days': total_completed_meal_days,
            'weights_list': weights_list,
        }, status=status.HTTP_200_OK)




class Aifeedback(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get user achievement, latest meal plan, and latest workout plan",
        operation_description="Fetch the authenticated user's achievement details, the latest completed meal plan, and the latest completed workout plan, including their progress.",
        responses={
            200: openapi.Response(
                description="Successfully fetched achievement and plans",
                schema=UserAchievementSerializer,
            ),
            404: openapi.Response(
                description="Not Found: No achievement or plans found for the user",
                examples={"application/json": {"detail": "Not found."}},
            ),
            400: openapi.Response(
                description="Bad Request: Invalid or incomplete request",
                examples={"application/json": {"detail": "Invalid request."}},
            ),
        },
        tags=["User Achievement"]
    )
    def get(self, request, *args, **kwargs):
        # Get the authenticated user
        user = request.user

        # Get the latest completed MealPlan
        latest_meal_plan = MealPlan.objects.filter(user=user, is_completed=True).order_by('-end_date').first()

        # Get the latest completed WorkoutPlan
        latest_workout_plan = WorkoutPlan.objects.filter(user=user, is_completed=True).order_by('-end_date').first()

        # Get the Achievement of the user
        achievement = Achievement.objects.filter(user=user).first()

        # Count total completed workout days for the latest workout plan
        total_completed_workout_days = DailyWorkout.objects.filter(
            workout_plan=latest_workout_plan, completed=True
        ).count() if latest_workout_plan else 0

        # Count total completed meal days for the latest meal plan
        total_completed_meal_days = DailyMeal.objects.filter(
            meal_plan=latest_meal_plan
        ).filter(
            meals__completed=True
        ).distinct().count() if latest_meal_plan else 0

        # Get fitness profile and weight data
        fitness_profiles = FitnessProfile.objects.filter(user=user)
        weights_list = [profile.current_weight for profile in fitness_profiles]

        # Prepare the data to send in response
        data = {
            'total_completed_workout_days': total_completed_workout_days,
            'total_completed_meal_days': total_completed_meal_days,
            'weights_list': weights_list,
        }
        feedbacks={}

        # If an achievement exists, serialize it and add it to the response data
        if achievement:
            achievement_serializer = AchievementSerializer(achievement)
            data['achievement'] = achievement_serializer.data  # Add the serialized achievement data

            # Generate feedback using OpenAI
            try:
                openai.api_key = settings.OPENAI_API_KEY
                # Create a prompt based on the user's data
                prompt = f"""User has completed {total_completed_workout_days} workout days and {total_completed_meal_days} meal days.
                Their current weight list is {weights_list}. Give positive and motivational feedback in Markdown format.
                After each sentence, add a new line (\\n).
                for this achievement without headings.must Add emoji not use ranbow emoji. Provide feedback in both English and Spanish in the format:
                "feedback_en": "<English Feedback>",
                "feedback_es": "<Spanish Feedback>"
                Please avoid adding any extra JSON formatting or tags
                """

                # Use the correct chat model endpoint
                response = openai.ChatCompletion.create(
                    model="gpt-4o",  # You can use gpt-3.5-turbo as well
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=0
                )

                # Get feedback from the response
                feedback = response.choices[0].message['content'].strip()

                feedback_en = feedback.split("feedback_es")[0].strip().replace('feedback_en', '').strip().strip(':')
                feedback_es = feedback.split("feedback_es")[1].strip().replace('feedback_es', '').strip().strip(':"')

                # Add the feedback to the response data
                feedbacks['feedback_en'] = feedback_en
                feedbacks['feedback_es'] = feedback_es

            except Exception as e:
                feedbacks['feedback_en'] = f"Error generating feedback: {str(e)}"
                feedbacks['feedback_es'] = f"Error generating feedback: {str(e)}"
                feedbacks['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(feedbacks, status=status.HTTP_200_OK)
