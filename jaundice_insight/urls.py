
from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.jaundice_check, name='jaundice_check'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('clear/', views.clear_prediction_history, name='clear_prediction_history'),
]
