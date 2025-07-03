from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RegisterApiView,LoginAPIView,CustomTokenRefreshView,ProfileViewSet


router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
