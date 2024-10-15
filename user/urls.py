from django.urls import path
from .views import UserRegistrationView, CustomUserLoginView
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', CustomUserLoginView.as_view()),
    path('logout/', TokenBlacklistView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
]

