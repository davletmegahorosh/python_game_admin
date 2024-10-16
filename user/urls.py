from django.urls import path
from .views import UserRegistrationView
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),

    path('login/', TokenObtainPairView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
]

