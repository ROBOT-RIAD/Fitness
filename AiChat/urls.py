from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamingChatAPIView
router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('Ai/',  StreamingChatAPIView.as_view(), name='chat'),
]