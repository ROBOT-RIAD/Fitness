from django.shortcuts import render
from rest_framework import generics,viewsets,status
from rest_framework.generics import CreateAPIView
from .models import User
from .models import Profile
from .serializers import RegisterSerializer,CustomTokenObtainPairSerializer,ProfileSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

#$swagger
from drf_yasg.utils import swagger_auto_schema

#jwt
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


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





# class GetProfileView(generics.RetrieveAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user.profile

#     @swagger_auto_schema(
#         operation_description="Retrieve the current user's profile.",
#         responses={200: ProfileSerializer()}
#     )
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class UpdateProfileView(generics.UpdateAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user.profile

#     @swagger_auto_schema(
#         operation_description="Update the current user's profile.",
#         request_body=ProfileSerializer,
#         responses={200: ProfileSerializer()}
#     )
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)




