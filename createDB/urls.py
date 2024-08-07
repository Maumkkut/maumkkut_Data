from django.urls import path
from . import views

urlpatterns = [
  path('save-tour-12/', views.save_tour_12, name='save_tour'),
  path('fetch_and_save_tours/',views.fetch_and_save_tours,name='fetch_and_save_tours'),
  path('save_tours_to_db/',views.save_tours_to_db, name="save_tours_to_db"),
  path('recommend-course/', views.recommend_course_view, name='recommend-course'),
  # path('recommend-group-course/', views.recommend_group_course_view, name='recommend-group-course'),
]