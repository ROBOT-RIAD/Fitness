from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import TermsAndConditions, PrivacyPolicy
from .serializers import TermsAndConditionsSerializer, PrivacyPolicySerializer
from accounts.permissions import IsAdminRole
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
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