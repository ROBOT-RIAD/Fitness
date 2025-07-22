from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,generics
from datetime import date, timedelta
from workout.models import Workout
from workout.serializers import WorkoutSerializer
from .models import WorkoutPlan, DailyWorkout, WorkoutEntry
from workout.models import Workout,WorkoutSpanish
from accounts.models import Profile
from accounts.permissions import IsUserRole
from .serializers import TrainingDataSerializer,WorkoutEntrySerializer, WorkoutEntryUpdateSerializer
from .services import build_workout_plan

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import calendar
from decimal import Decimal

class GenerateWorkoutPlanView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=TrainingDataSerializer,
        operation_summary="Generate a 15-Day AI-Powered Workout Plan",
        operation_description="""
        Generates a personalized 15-day workout plan using OpenAI based on the authenticated user's profile,
        training preferences, and available workouts.

        🔐 Requires authentication  
        🧠 Uses OpenAI (GPT-4)  
        📌 Saves full plan to database
        """,
        tags=["AI Workout Plan"],
        responses={
            201: openapi.Response(
                description="Workout plan created successfully",
                examples={
                    "application/json": {
                        "detail": "Workout plan created successfully",
                        "workout_plan_id": 101,
                        "workout_plan_name": "Lean Strength Plan",
                        "tags": "strength,endurance,home"
                    }
                }
            ),
            400: openapi.Response(description="Invalid training data"),
            404: openapi.Response(description="User profile not found"),
            500: openapi.Response(description="OpenAI error or internal failure")
        }
    )
    def post(self, request):
        user = request.user

        # 1. Validate user profile
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=404)

        # 2. Validate training input
        serializer = TrainingDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        training_data = serializer.validated_data

        # 3. Get all valid workouts
        workouts_qs = Workout.objects.exclude(unique_id__isnull=True).exclude(unique_id__exact="")

        # 4. Call OpenAI to build the plan
        try:
            result = build_workout_plan(profile, training_data, workouts_qs, days=15)
            workout_plan_name = result.get("workout_plan_name", "15-Day AI Plan")
            tags = result.get("tags", "")
            plan_days = result.get("days", [])
        except Exception as e:
            return Response({"detail": f"OpenAI error: {str(e)}"}, status=500)

        # 5. Create WorkoutPlan instance
        today = date.today()
        workout_plan = WorkoutPlan.objects.create(
            user=user,
            workout_plan_name=workout_plan_name,
            tags=tags,
            start_date=today,
            end_date=today + timedelta(days=14),
        )

        # 6. Cache workouts for quick lookup
        uid_cache = {w.unique_id: w for w in workouts_qs}

        # 7. Create DailyWorkout and WorkoutEntry entries
        for day in plan_days:
            daily = DailyWorkout.objects.create(
                workout_plan=workout_plan,
                date=day["date"],
                title=day.get("title", f"Workout - {day['date']}"),
                title_spanish=day.get("title_spanish", day.get("title", "")),
                tags=day.get("tags", tags),
                tags_spanish=day.get("tags_spanish", day.get("tags", "")),
            )
            for w in day.get("workouts", []):
                workout = uid_cache.get(w["workout_uid"])
                WorkoutEntry.objects.create(
                    daily_workout=daily,
                    workout=workout,
                    completed=False,
                    set_of=w.get("set_of", 1),
                    reps=w.get("reps", 10)
                )


        # 8. Return response
        return Response({
            "detail": "Workout plan created successfully",
            "workout_plan_id": workout_plan.id,
            "workout_plan_name": workout_plan_name,
            "tags": tags
        }, status=status.HTTP_201_CREATED)



class ActiveWorkoutPlanView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get active workout plan",
        operation_description="Returns day-wise info for the user's active workout plan (is_completed=False, is_cancelled=False)",
        tags=["Day wise workout"],
        responses={
            200: openapi.Response(
                description="Active workout plan details",
                examples={
                    "application/json": {
                        "days": [
                            {
                                "id": 1,
                                "title": "Chest Day",
                                "title_spanish": "Día de Pecho",
                                "tags": "chest,strength",
                                "tags_spanish": "pecho,fuerza",
                                "completed": False,
                                "day": "Day 1",
                                "weekday": "Saturday",
                                "total_minutes": 45,
                                "total_calories_burned": 350
                            }
                        ],
                        "status": {
                            "total_days": 15,
                            "average_time": 40,
                            "total_workouts": 45
                        }
                    }
                }
            ),
            404: openapi.Response(description="No active workout plan found")
        }
    )
    def get(self, request):
        user = request.user

        try:
            workout_plan = WorkoutPlan.objects.get(
                user=user, is_completed=False, is_cancelled=False
            )
        except WorkoutPlan.DoesNotExist:
            return Response({"detail": "No active workout plan found."}, status=404)

        days_info = []
        total_minutes_all = 0
        total_workout_count = 0

        for daily in workout_plan.daily_workouts.all().order_by("date"):
            total_minutes = 0
            total_calories = 0

            for entry in daily.workouts.all():
                if entry.workout:
                    duration = entry.workout.time_needed
                    if isinstance(duration, timedelta):
                        total_minutes += int(duration.total_seconds() / 60)
                    total_calories += float(entry.workout.calories_burn)
                    total_workout_count += 1

            total_minutes_all += total_minutes

            day_diff = (daily.date - workout_plan.start_date).days
            day_number = day_diff + 1
            weekday_name = calendar.day_name[daily.date.weekday()]

            days_info.append({
                "id": daily.id,
                "title": daily.title,
                "title_spanish": daily.title_spanish,
                "tags": daily.tags,
                "tags_spanish": daily.tags_spanish,
                "date": daily.date,
                "completed": daily.completed,
                "day": f"Day {day_number}",
                "weekday": weekday_name,
                "total_minutes": total_minutes,
                "total_calories_burned": round(total_calories, 2),
            })

        total_days = workout_plan.daily_workouts.count()
        average_time = round(total_minutes_all / total_days, 2) if total_days else 0

        return Response({
            "days": days_info,
            "status": {
                "total_days": total_days,
                "average_time": average_time,
                "total_workouts": total_workout_count
            }
        })


class CompleteTodayWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Mark today's workout as completed or not",
        operation_description="User can mark their today's active daily workout as completed or not completed.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="True to mark as completed, False to unmark")
            },
            required=['completed']
        ),
        tags=["Day wise workout"],
        responses={
            200: openapi.Response(
                description="Workout status updated",
                examples={
                    "application/json": {
                        "detail": "Today's workout marked as completed.",
                        "id": 10,
                        "date": "2025-07-20",
                        "title": "Leg Day",
                        "completed": True
                    }
                }
            ),
            400: "Invalid input",
            404: "No active workout plan or workout for today found"
        },
    )
    def patch(self, request):
        user = request.user
        completed = request.data.get("completed")

        if completed is None:
            return Response({"detail": "Missing 'completed' field in request body."}, status=400)

        if not isinstance(completed, bool):
            return Response({"detail": "'completed' must be true or false."}, status=400)

        try:
            workout_plan = WorkoutPlan.objects.get(user=user, is_completed=False, is_cancelled=False)
        except WorkoutPlan.DoesNotExist:
            return Response({"detail": "No active workout plan found."}, status=404)

        try:
            daily_workout = workout_plan.daily_workouts.get(date=date.today())
        except DailyWorkout.DoesNotExist:
            return Response({"detail": "No workout scheduled for today."}, status=404)

        daily_workout.completed = completed
        daily_workout.save()

        return Response({
            "detail": f"Today's workout marked as {'completed' if completed else 'not completed'}.",
            "id": daily_workout.id,
            "date": daily_workout.date,
            "title": daily_workout.title,
            "completed": daily_workout.completed
        }, status=200)



class DailyWorkoutDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get details of a daily workout",
        responses={200: "Success", 404: "Not Found"},
        tags=["single day all workout"]
    )
    def get(self, request, pk):
        try:
            daily_workout = DailyWorkout.objects.get(id=pk, workout_plan__user=request.user)
        except DailyWorkout.DoesNotExist:
            return Response({"detail": "Daily workout not found."}, status=status.HTTP_404_NOT_FOUND)

        workout_entries = WorkoutEntry.objects.filter(daily_workout=daily_workout).select_related('workout')
        serializer = WorkoutEntrySerializer(workout_entries, many=True)

        # Summary calculations
        total_duration_minutes = 0
        total_calories = 0

        for entry in workout_entries:
            workout = entry.workout
            if workout.time_needed:
                total_duration_minutes += int(workout.time_needed.total_seconds() // 60)
            if workout.calories_burn:
                total_calories += float(workout.calories_burn)

        return Response({
            "workouts": serializer.data,
            "status": {
                "total_workout": workout_entries.count(),
                "total_duration_minutes": total_duration_minutes,
                "total_calories_burn": total_calories
            }
        }, status=200)




class SpanishDailyWorkoutDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get details of a daily workout (Spanish)",
        responses={200: "Success", 404: "Not Found"},
        tags=["single day all workout"]
    )
    def get(self, request, pk):
        try:
            daily_workout = DailyWorkout.objects.get(id=pk, workout_plan__user=request.user)
        except DailyWorkout.DoesNotExist:
            return Response({"detail": "Daily workout not found."}, status=status.HTTP_404_NOT_FOUND)

        workout_entries = WorkoutEntry.objects.filter(daily_workout=daily_workout).select_related('workout')
        
        total_duration_minutes = 0
        total_calories = 0
        response_data = []

        for entry in workout_entries:
            workout = entry.workout
            spanish_workout = WorkoutSpanish.objects.filter(unique_id=workout.unique_id).first()

            if spanish_workout:
                duration = spanish_workout.time_needed.total_seconds() // 60 if spanish_workout.time_needed else 0
                calories = float(spanish_workout.calories_burn) if spanish_workout.calories_burn else 0
            else:
                duration = 0
                calories = 0

            total_duration_minutes += duration
            total_calories += calories

            response_data.append({
                "entry_id": entry.id,
                "set_of": entry.set_of,
                "reps": entry.reps,
                "completed": entry.completed,
                "workout": {
                    "id": spanish_workout.id if spanish_workout else None,
                    "unique_id": workout.unique_id,
                    "workout_name": spanish_workout.workout_name if spanish_workout else None,
                    "time_needed": str(spanish_workout.time_needed) if spanish_workout else None,
                    "for_body_part": spanish_workout.for_body_part if spanish_workout else None,
                    "workout_type": spanish_workout.workout_type if spanish_workout else None,
                    "calories_burn": spanish_workout.calories_burn if spanish_workout else None,
                    "equipment_needed": spanish_workout.equipment_needed if spanish_workout else None,
                    "tag": spanish_workout.tag if spanish_workout else None,
                    "benefits": spanish_workout.benefits if spanish_workout else None,
                    "image": request.build_absolute_uri(spanish_workout.image.url) if spanish_workout and spanish_workout.image else None,
                }
            })

        return Response({
            "workouts": response_data,
            "status": {
                "total_workout": workout_entries.count(),
                "total_duration_minutes": total_duration_minutes,
                "total_calories_burn": total_calories
            }
        }, status=200)
    


class TodayWorkoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get Today's workout",
        responses={200: "Success", 404: "Not Found"},
        tags=["Today Workout"]
    )
    def get(self, request):
        today = date.today()

        # Get all DailyWorkouts for the user
        all_daily_workouts = DailyWorkout.objects.filter(
            workout_plan__user=request.user
        )

        # Count completed days
        total_completed_days = all_daily_workouts.filter(completed=True).count()

        # Today's workout entries
        entries = WorkoutEntry.objects.filter(
            daily_workout__date=today,
            daily_workout__workout_plan__user=request.user
        ).select_related('workout', 'daily_workout')

        workouts_data = []
        total_duration = 0
        total_calories = 0

        for entry in entries:
            if entry.workout:
                workout = entry.workout
                duration_minutes = workout.time_needed.total_seconds() / 60
                calories = float(workout.calories_burn)

                workouts_data.append({
                    "date": entry.daily_workout.date,
                    "set_of": entry.set_of,
                    "reps": entry.reps,
                    "completed": entry.completed,
                    "workout": {
                        "workout_name": workout.workout_name,
                        "time_needed": str(workout.time_needed),
                        "for_body_part": workout.for_body_part,
                        "workout_type": workout.workout_type,
                        "calories_burn": str(workout.calories_burn),
                        "equipment_needed": workout.equipment_needed,
                        "tag": workout.tag,
                        "image": workout.image.url if workout.image else None,
                        "benefits": workout.benefits,
                        "unique_id": workout.unique_id,
                    }
                })

                total_duration += duration_minutes
                total_calories += calories

        return Response({
            "workouts": workouts_data,
            "status": {
                "total_workout": len(workouts_data),
                "total_duration_minutes": int(total_duration),
                "total_calories_burn": int(total_calories),
                "total_completed_days": total_completed_days
            }
        })
    


class SpanishWorkoutEntryListView(APIView):
    @swagger_auto_schema(
        operation_summary="Get Today's workout",
        responses={200: "Success", 404: "Not Found"},
        tags=["Today Workout"]
    )
    def get(self, request):
        user = request.user
        today = date.today()

        # Filter today's entries of current user
        entries = WorkoutEntry.objects.filter(
            daily_workout__workout_plan__user=user,
            daily_workout__date=today
        ).select_related('daily_workout', 'workout')  # optimization

        workouts_data = []
        total_duration = 0
        total_calories = Decimal('0.00')
        total_completed_days = DailyWorkout.objects.filter(
            workout_plan__user=user,
            completed=True
        ).count()

        for entry in entries:
            # Match WorkoutSpanish using unique_id
            if entry.workout:
                try:
                    spanish = WorkoutSpanish.objects.get(unique_id=entry.workout.unique_id)
                except WorkoutSpanish.DoesNotExist:
                    continue

                duration_minutes = spanish.time_needed.total_seconds() / 60
                total_duration += duration_minutes
                total_calories += spanish.calories_burn

                workouts_data.append({
                    "completed": entry.completed,
                    "set_of": entry.set_of,
                    "reps": entry.reps,
                    "date": entry.daily_workout.date,
                    "workout":{
                        "workout_name": spanish.workout_name,
                        "time_needed": str(spanish.time_needed),
                        "for_body_part": spanish.for_body_part,
                        "workout_type": spanish.workout_type,
                        "calories_burn": float(spanish.calories_burn),
                        "equipment_needed": spanish.equipment_needed,
                        "tag": spanish.tag,
                        "image" : spanish.image.url,
                        "benefits":spanish.benefits,
                        "unique_id":spanish.unique_id,

                    },
                })

        return Response({
            "workouts": workouts_data,
            "status": {
                "total_workout": len(workouts_data),
                "total_duration_minutes": int(total_duration),
                "total_calories_burn": int(total_calories),
                "total_completed_days": total_completed_days
            }
        })
    



class UpdateTodayWorkoutEntryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Partially update today's workout entry",
        operation_description="PATCH: Partially update a WorkoutEntry instance for today belonging to the authenticated user.",
        tags=["Today Workout"],
        request_body=WorkoutEntryUpdateSerializer,
        responses={
            200: openapi.Response("Workout entry updated successfully.", WorkoutEntryUpdateSerializer),
            400: "Bad Request",
            403: "Forbidden",
            404: "Not Found"
        },
    )
    def patch(self, request, pk):
        user = request.user
        today = date.today()

        try:
            entry = WorkoutEntry.objects.get(
                pk=pk,
                daily_workout__workout_plan__user=user,
                daily_workout__date=today
            )
        except WorkoutEntry.DoesNotExist:
            return Response({"detail": "Workout entry not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = WorkoutEntryUpdateSerializer(entry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)