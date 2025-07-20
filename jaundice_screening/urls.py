from django.urls import path
from . import views

urlpatterns = [
    path('', views.screening_view, name='screening_view'),
]
