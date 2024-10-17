from django.urls import path, include
from .views import TournamentCreate

urlpatterns = [
    path('create_tournament/', TournamentCreate.as_view()),
]
