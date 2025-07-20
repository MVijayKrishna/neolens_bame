from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('case/<int:pk>/', views.case_detail, name='case_detail'),
    path('comparison/', views.comparison_tool, name='comparison_tool'),
    path('checker/', views.jaundice_checker, name='jaundice_checker'),
]
