from django.shortcuts import render
from rest_framework import generics,viewsets,status
from rest_framework.generics import CreateAPIView
from .models import User,Profile,PasswordResetOTP
from .models import Profile
from .serializers import RegisterSerializer,CustomTokenObtainPairSerializer,ProfileSerializer,SendOTPSerializer,VerifyOTPSerializer,ResetPasswordSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings

#$swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser


#jwt
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

#openai
import openai
openai.api_key = settings.OPENAI_API_KEY
import json

# Create your views here.


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    @swagger_auto_schema(tags=["Authentication"])

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'name': user.profile.fullname if hasattr(user, 'profile') else '',
                }
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response({"errors": ve.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class LoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    @swagger_auto_schema(tags=["Authentication"])
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request,*args,**kwargs)
        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e :
            return Response({"error": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)



class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=["Authentication"])
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e :
            return Response({"error":str(e)} , status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser,JSONParser]

    def get_object(self):
        # Ensure a Profile exists for the user
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    @swagger_auto_schema(
        responses={200: ProfileSerializer()}
    )
    @action(detail=False, methods=['get'])
    def get_profile(self, request):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_id="patch_profile_me",
        operation_summary="Update the current user's profile",
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer()}
    )
    @action(detail=False, methods=['patch'])
    def patch_profile(self, request):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_id="delete_profile_me",
        operation_summary="Delete the current user's profile",
        responses={204: 'Profile deleted successfully'}
    )
    @action(detail=False, methods=['delete'])
    def delete_profile(self, request):
        profile = self.get_object()
        profile.delete()
        return Response({"detail": "Profile deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    


    @swagger_auto_schema(
        method='post',
        operation_id="ai_recommended_data",
        operation_summary="Get AI-generated health recommendations",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
        ),
        responses={
            200: openapi.Response(
                description="AI-generated health data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "perfect_weight_kg": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "abdominal": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "triceps": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "subscapular": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "suprailiac": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "total_calories_per_day": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "water_need_liters_per_day": openapi.Schema(type=openapi.TYPE_NUMBER),
                        "sleep_need_hours_per_day": openapi.Schema(type=openapi.TYPE_INTEGER)
                    }
                )
            ),
            500: "OpenAI failed"
        }
    )
    @action(detail=False, methods=['post'])
    def ai_recommended_data(self, request):
        profile = self.get_object()

        # Use validated data if passed, fallback to profile values
        data = request.data
        
        input_data = {
                "fullname": data.get("fullname", profile.fullname),
                "gender": data.get("gender", profile.gender),
                "date_of_birth": str(data.get("date_of_birth", profile.date_of_birth)),

                "weight": data.get("weight", profile.weight),
                "height": data.get("height", profile.height),
                "abdominal": data.get("abdominal", profile.abdominal),
                "sacroiliac": data.get("sacroiliac", profile.sacroiliac),
                "subscapularis": data.get("subscapularis", profile.subscapularis),
                "triceps": data.get("triceps", profile.triceps),

                "fitness_level": data.get("fitness_level", profile.fitness_level),
                "trainer": data.get("trainer", profile.trainer),

                "at_home": data.get("at_home", profile.at_home),
                "at_gym": data.get("at_gym", profile.at_gym),
                "martial_arts": data.get("martial_arts", profile.martial_arts),
                "running": data.get("running", profile.running),
                "other_sports": data.get("other_sports", profile.other_sports),

                "train_duration": data.get("train_duration", profile.train_duration),
                "interested_workout": data.get("interested_workout", profile.interested_workout),
                "injuries_discomfort": data.get("injuries_discomfort", profile.injuries_discomfort),

                "routine_duration": data.get("routine_duration", profile.routine_duration),
                "dietary_preferences": data.get("dietary_preferences", profile.dietary_preferences),
                "allergies": data.get("allergies", profile.allergies),
                "food_preference": data.get("food_preference", profile.food_preference),
                "medical_conditions": data.get("medical_conditions", profile.medical_conditions),
                "fitness_goals": data.get("fitness_goals", profile.fitness_goals),
                "lifestyle_habits": data.get("lifestyle_habits", profile.lifestyle_habits),

        }


        prompt = f"""
    You are a fitness expert. Based on this JSON profile:
    {json.dumps(input_data, indent=2)}

    Return JSON with only:
    - perfect_weight_kg
    - abdominal
    - triceps
    - subscapular
    - suprailiac (same as sacroiliac)
    - total_calories_per_day
    - water_need_liters_per_day
    - sleep_need_hours_per_day

    Use only raw JSON. Do not explain anything.
    """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                temperature=0,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content.strip()
            recommended_data = json.loads(content)
            return Response(recommended_data, status=200)
        except Exception as e:
            return Response({"error": "OpenAI failed", "detail": str(e)}, status=500)






class SendOTPView(APIView):
    permission_classes = [AllowAny]
 
    @swagger_auto_schema(
        request_body=SendOTPSerializer,
        tags=["Forgot Password"],
        operation_summary="Send OTP to email",
        responses={200: openapi.Response('OTP sent'), 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            otp_record = PasswordResetOTP.objects.create(user=user)
        
            # print(otp_record.otp)
            print(email)


            # Send OTP via email
            send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is: {otp_record.otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            )

            return Response({
                "message": "OTP sent to your email.",
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        tags=["Forgot Password"],
        operation_summary="Verify OTP",
        responses={200: openapi.Response('OTP verified'), 400: 'Invalid OTP'}
    )

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp_record = PasswordResetOTP.objects.filter(
                user=user, otp=otp, is_verified=False
            ).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        otp_record.is_verified = True
        otp_record.save()

        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
    






class ResetPasswordView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(
        request_body=ResetPasswordSerializer,
        manual_parameters=[
            openapi.Parameter(
                'email',
                openapi.IN_QUERY,
                description="Email address to reset password for",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        tags=["Forgot Password"],
        operation_summary="Reset password after OTP verification",
        responses={200: openapi.Response('Password reset successful'), 400: 'Bad Request'}
    )

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email is required in query params."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            otp_record = PasswordResetOTP.objects.filter(
                user=user, is_verified=True
            ).latest('created_at')
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "OTP not verified or expired."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            otp_record.delete()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error" : e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)