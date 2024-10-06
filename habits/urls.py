from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, RegisterView

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token-auth/', drf_views.obtain_auth_token, name='token-auth'),
]
