from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import TermsAndConditions, PrivacyPolicy,Email
from .serializers import TermsAndConditionsSerializer, PrivacyPolicySerializer,EmailSerializer
from accounts.permissions import IsAdminRole
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.


class TermsAndConditionsViewSet(ModelViewSet):
    queryset = TermsAndConditions.objects.all()
    serializer_class = TermsAndConditionsSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    @swagger_auto_schema(tags=["terms and privacy"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["terms and privacy"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["terms and privacy"])
    def create(self, request, *args, **kwargs):
        if self.queryset.exists():
            return Response(
                {"detail": "Only one Terms and Conditions record is allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["terms and privacy"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["terms and privacy"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




class PrivacyPolicyViewSet(ModelViewSet):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    @swagger_auto_schema(tags=["terms and privacy"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["terms and privacy"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["terms and privacy"])
    def create(self, request, *args, **kwargs):
        if self.queryset.exists():
            return Response(
                {"detail": "Only one Terms and Conditions record is allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["terms and privacy"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["terms and privacy"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




class TermsAndConditionsView(APIView):
    permission_classes = [AllowAny]  # Public access

    @swagger_auto_schema(
        operation_summary="Get the Terms and Conditions",
        operation_description="Fetch the terms and conditions of the application.",
        responses={
            200: openapi.Response(description="Terms and Conditions fetched successfully", schema=TermsAndConditionsSerializer),
            404: openapi.Response(description="Terms and Conditions not found")
        },
        tags=["Privacy Policy public"]
    )
    def get(self, request):
        terms = TermsAndConditions.objects.first()  # Get the first instance of Terms and Conditions
        if terms:
            serializer = TermsAndConditionsSerializer(terms)
            return Response(serializer.data)
        return Response({"error": "Terms and Conditions not found"}, status=404)




class PrivacyPolicyView(APIView):
    permission_classes = [AllowAny]  # Public access

    @swagger_auto_schema(
        operation_summary="Get the Privacy Policy",
        operation_description="Fetch the privacy policy of the application.",
        responses={
            200: openapi.Response(description="Privacy Policy fetched successfully", schema=PrivacyPolicySerializer),
            404: openapi.Response(description="Privacy Policy not found")
        },
        tags=["Privacy Policy public"]
    )
    def get(self, request):
        privacy_policy = PrivacyPolicy.objects.first()  # Get the first instance of Privacy Policy
        if privacy_policy:
            serializer = PrivacyPolicySerializer(privacy_policy)
            return Response(serializer.data)
        return Response({"error": "Privacy Policy not found"}, status=404)
    

    

class SendEmailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Send an email to admin",
        operation_description="This endpoint allows an authenticated user to send an email to the admin. "
                              "The user provides the body and subject of the email. The email is then sent, "
                              "and the record is stored in the database.",
        request_body=EmailSerializer,
        responses={
            201: openapi.Response(
                description="Email sent successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Response message'),
                        'email_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the created email record')
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            ),
            500: openapi.Response(
                description="Internal Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Error message'),
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Detailed error')
                    }
                )
            )
        },
        tags=["Email"]
    )

    def post(self, request, *args, **kwargs):
        # Get data from the request
        serializer = EmailSerializer(data=request.data)
        
        if serializer.is_valid():
            email_data = serializer.validated_data
            
            # Get the email body, subject, and the user sending the email
            body = email_data.get('body')
            subject = email_data.get('subject', 'No Subject')  # Default subject if not provided
            user = request.user
            admin_email = settings.EMAIL_HOST_USER

            # Send the email (adjust recipient list as needed)
            try:
                send_mail(
                    subject,
                    body,
                    user.email,  # Sending user's email address
                    [admin_email],  # Email to admin (you can add multiple email addresses here)
                    fail_silently=False
                )
                
                # Save the email record
                email = Email.objects.create(user=user, subject=subject, body=body, sent_status=True)
                
                return Response({
                    "message": "Email sent successfully!",
                    "email_id": email.id
                }, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                # Save the email record with failed status
                email = Email.objects.create(user=user, subject=subject, body=body, sent_status=False)
                
                return Response({
                    "message": "Failed to send email.",
                    "error": str(e),
                    "email_id": email.id
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


