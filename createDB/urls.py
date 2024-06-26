from django.urls import path
from . import views

urlpatterns = [
  path('save-tour-12/', views.save_tour_12, name='save_tour'),
]