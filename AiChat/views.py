# views.py
from django.shortcuts import render
from django.conf import settings
import openai
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
import time
import logging
from accounts.models import Profile
from meal.models import MealPlan, DailyMeal, MealEntry
from workoutplan.models import WorkoutPlan,DailyWorkout,WorkoutEntry
from recipe.models import Recipe
from datetime import date, timedelta
import re
from dateutil.parser import parse

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Configure logging
logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY

# System prompt
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a professional health and fitness advisor. "
        "User help cooking her recipe informations"
        "Provide accurate, safe advice on diet, exercise, and meal planning. "
        "Respond to every user message with a new, relevant response."
    )
}

SESSION_CHAT_HISTORY = {}
print(SESSION_CHAT_HISTORY)

def get_requested_date(user_input):
    """
    Parse the user's input to detect if they are asking for today's, tomorrow's, or any other specific date.
    Handles formats like '5 August', 'August 5', '5th August', '2025-08-05', etc.
    """
    user_input = user_input.lower()
    user_input = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', user_input)  # Remove ordinal suffixes

    if "today" in user_input:
        return date.today()
    elif "tomorrow" in user_input:
        return date.today() + timedelta(days=1)
    elif "yesterday" in user_input:
        return date.today() - timedelta(days=1)

    try:
        parsed_date = parse(user_input, fuzzy=True).date()
        if parsed_date.year < 2000 or parsed_date.year > date.today().year + 5:
            parsed_date = parsed_date.replace(year=date.today().year)
        logger.info(f"Parsed date from input '{user_input}': {parsed_date}")
        return parsed_date
    except ValueError:
        logger.warning(f"Could not parse date from input: {user_input}. Defaulting to today.")
        return date.today()


class StreamingChatAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        operation_description="Stream AI chatbot response for health & fitness advice, including today's meal plan if requested.",
        tags=["Health Chatbot"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["message"],
            properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="User message to the health chatbot"),
                "session_id": openapi.Schema(type=openapi.TYPE_STRING, description="Unique session ID (optional)")
            },
        ),
        responses={200: "Streaming text response"}
    )
    def post(self, request):
        user_input = request.data.get("message")
        session_id = request.data.get("session_id", str(time.time()))  # Unique session_id if not provided

        if not user_input:
            return StreamingHttpResponse("error: no input", status=400)

        # Initialize or get chat history
        if session_id not in SESSION_CHAT_HISTORY:
            SESSION_CHAT_HISTORY[session_id] = [SYSTEM_PROMPT]
        else:
            # Ensure the system prompt is always included
            if SESSION_CHAT_HISTORY[session_id][0] != SYSTEM_PROMPT:
                SESSION_CHAT_HISTORY[session_id].insert(0, SYSTEM_PROMPT)

        chat_history = SESSION_CHAT_HISTORY[session_id]

        max_history_length = 5
        chat_history = chat_history[-max_history_length:]

        requested_date = get_requested_date(user_input)
        print(requested_date)
        logger.info(f"Requested date for meal plan: {requested_date}")

        # Inject personalized data if authenticated
        profile = Profile.objects.get(user=request.user)

        # Build profile summary (basic, for context)
        profile_summary = f"""
                User Profile:
                - Name: {profile.fullname or 'Not provided'}
                - gender: {profile.gender or 'Not provided'}
                - date_of_birth: {profile.date_of_birth or 'Not provided'}
                - weight: {profile.weight or 'Not provided'}
                - height: {profile.height or 'Not provided'}
                - abdominal: {profile.abdominal or 'Not provided'}
                - sacroiliac: {profile.sacroiliac or 'Not provided'}
                - subscapularis: {profile.subscapularis or 'Not provided'}
                - triceps: {profile.triceps or 'Not provided'}
                - fitness_level: {profile.fitness_level or 'Not provided'}
                - interested_workout: {profile.interested_workout or 'Not provided'}
                - injuries_discomfort: {profile.injuries_discomfort or 'Not provided'}
                - medical_conditions: {profile.medical_conditions or 'Not provided'}
                - Dietary Preferences: {profile.dietary_preferences or 'Not provided'}
                - Allergies: {', '.join(profile.allergies) if profile.allergies else 'None'}
                - Fitness Goals: {', '.join(profile.fitness_goals) if profile.fitness_goals else 'Not provided'}
        """
        
        # Call the function to get meal plan summary
        meal_plan_summary = self.get_meal_plan_summary(request, requested_date)
        workout_plan_summary = self.get_workout_plan_summary(request, requested_date)
        
        full_context = {
            "role": "system",
            "content": f"""
                You are a professional health and fitness advisor AI.
                {profile_summary}
                {meal_plan_summary}
                {workout_plan_summary}   
                Provide a detailed summary of the user's meal plan for the requested date ({requested_date}), including all meal entries, recipes, and nutritional details. Ensure the response is accurate, encouraging, and tailored to the user's dietary preferences, allergies, and fitness goals. Do not omit any meal plan details unless explicitly requested.
                when you give response give the {meal_plan_summary} in the response when the user asks for her meal plan or any sort of meal plan..strictly follow this rule..
                {meal_plan_summary} must be send  Meal,Recipe,Category,Type,For,Tags,Eating Time,Total Food Weight for Today,Ingredients,Ingredients_weight,InstructionsCompleted,..
                Ingredients_weight must be send..
                Eating Time show as 12 hours..
            """
        }

        # Insert user context after the system prompt
        chat_history.insert(1, full_context)

        # Add user message
        chat_history.append({"role": "user", "content": user_input})

        logger.info(f"Received message: {user_input}, session_id: {session_id}")

        # Define a generator to stream the response
        def event_stream():
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-5-nano",
                    messages=chat_history,
                    # temperature=0.1,
                    stream=True
                )

                full_reply = ""
                for chunk in response:
                    if 'choices' in chunk and len(chunk['choices']) > 0:
                        delta = chunk['choices'][0]['delta']
                        if 'content' in delta:
                            content = delta['content']
                            full_reply += content
                            logger.debug(f"Streaming chunk: {content}")
                            yield content
                            time.sleep(0.05)  # Reduced delay for smoother streaming

                chat_history.append({"role": "assistant", "content": full_reply})
                logger.info(f"Completed response: {full_reply}, session_id: {session_id}")

            except Exception as e:
                error_msg = f"\n[ERROR]: {str(e)}"
                logger.error(f"Error in stream: {str(e)}, session_id: {session_id}")
                yield error_msg

        return StreamingHttpResponse(event_stream(), content_type='text/plain')

    def get_meal_plan_summary(self, request, requested_date):
        meal_plan_summary = ""
        if request.user and request.user.is_authenticated:
            try:
                active_plans = MealPlan.objects.filter(
                    user=request.user,
                    is_completed=False,
                    is_cancelled=False,        
                )

                # Log active plans for debugging
                logger.info(f"Requested date for meal plan: {requested_date}")
                logger.info(f"Active meal plans for today: {active_plans}")

                # Build meal plan summary for today
                if not active_plans:
                    meal_plan_summary = "No active meal plans for today."
                    logger.warning(f"No active meal plans for user: {request.user.email}")
                else:
                    for plan in active_plans:
                        meal_plan_summary += f"""
                            Active Meal Plan: '{plan.meal_plan_name}'
                            - Duration: {plan.start_date} to {plan.end_date}
                            - Tags: {plan.tags or 'None'}
                        """
                        # Fetch daily meals for today only
                        daily_meals = DailyMeal.objects.filter(meal_plan=plan, date=requested_date)
                        
                        logger.info(f"Today's daily meals: {daily_meals}")

                        if not daily_meals:
                            meal_plan_summary += "\nNo meals scheduled for today."
                            logger.warning(f"No meals scheduled for today for user: {request.user.email}")
                        else:
                            for daily_meal in daily_meals:
                                meal_plan_summary += f"\nToday's Meal Schedule ({daily_meal.date}):"
                                # Fetch meal entries for today
                                meal_entries = MealEntry.objects.filter(daily_meal=daily_meal)
                                logger.info(f"Meal entries for today: {meal_entries}")

                                if not meal_entries:
                                    meal_plan_summary += "\nNo meal entries for today."
                                    logger.warning(f"No meal entries found for user: {request.user.email}")
                                else:
                                    for entry in meal_entries:
                                        recipe = entry.recipe
                                        if recipe:
                                            meal_plan_summary += f"""
                                                - Meal: {entry.meal_type}
                                                - Recipe: {recipe.recipe_name}
                                                - Type: {recipe.recipe_type}
                                                - For: {recipe.for_time}
                                                - Eating Time: {entry.eating_time or 'Not specified'}
                                                - Total Food Weight for Today: {entry.grams if entry.grams else 'Not specified'}
                                                - Ingredients: {recipe.ingredients[:100] + '...' if recipe.ingredients else 'None'}
                                                - Calories: {recipe.calories} kcal
                                                - Protein: {recipe.protein}g
                                                - Carbs: {recipe.carbs}g
                                                - Fat: {recipe.fat}g
                                                - Instructions: {recipe.instructions[:100] + '...' if recipe.instructions else 'None'}
                                                - Completed: {entry.completed}
                                            """
                                        else:
                                            meal_plan_summary += f"""
                                                - Meal: {entry.meal_type}
                                                - No recipe linked.
                                                - Eating Time: {entry.eating_time or 'Not specified'}
                                                - Grams: {entry.grams or 'Not specified'}
                                                - Ingredients (EN): {entry.ingredients_en or 'Not provided'}
                                                - Ingredients (ES): {entry.ingredients_es or 'Not provided'}
                                                - Completed: {entry.completed}
                                                - Cancelled: {entry.cancelled}
                                            """
            except Exception as e:
                meal_plan_summary = f"Error retrieving meal plan: {str(e)}"
                logger.error(f"Error fetching meal plan for user {request.user.email}: {str(e)}")

        return meal_plan_summary

   
    
    def get_workout_plan_summary(self, request, requested_date):
        workout_plan_summary = ""
        if request.user and request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                active_workout_plans = WorkoutPlan.objects.filter(
                    user=request.user,
                    is_completed=False,
                    is_cancelled=False,
                )

                if not active_workout_plans:
                    workout_plan_summary = "No active workout plans for today."
                    logger.warning(f"No active workout plans for user: {request.user.email}")
                else:
                    for plan in active_workout_plans:
                        workout_plan_summary += f"""
                            Active Workout Plan: '{plan.workout_plan_name}'
                            - Duration: {plan.start_date} to {plan.end_date}
                            - Tags: {plan.tags or 'None'}
                        """

                        # Fetch daily workouts for today
                        daily_workouts = DailyWorkout.objects.filter(workout_plan=plan, date=requested_date)
                        
                        if not daily_workouts:
                            workout_plan_summary += "\nNo workouts scheduled for today."
                            logger.warning(f"No workouts scheduled for today for user: {request.user.email}")
                        else:
                            for daily_workout in daily_workouts:
                                workout_plan_summary += f"\nToday's Workout ({daily_workout.date}):"
                                # Fetch workout entries for today
                                workout_entries = WorkoutEntry.objects.filter(daily_workout=daily_workout)

                                if not workout_entries:
                                    workout_plan_summary += "\nNo workout entries for today."
                                    logger.warning(f"No workout entries found for user: {request.user.email}")
                                else:
                                    for entry in workout_entries:
                                        workout_plan_summary += f"""
                                            - Workout: {entry.workout.workout_name}
                                            - For body part: {entry.workout.for_body_part}
                                            - Time Needed: {entry.workout.time_needed}
                                            - workout type: {entry.workout.workout_type}
                                            - Calories Burn: {entry.workout.calories_burn}
                                            - Equipment Needed: {entry.workout.equipment_needed}
                                            - Benefits: {entry.workout.benefits}
                                            - Sets: {entry.set_of}
                                            - Reps: {entry.reps}
                                            - Completed: {entry.completed}
                                        """
            except Exception as e:
                logger.error(f"Failed to load workout data: {e}")
                workout_plan_summary = "Error retrieving workout plan data for today."

        return workout_plan_summary





