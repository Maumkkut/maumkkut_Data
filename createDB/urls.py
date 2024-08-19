from django.urls import path
from . import views

urlpatterns = [
  path('save-tour-12/', views.save_tour_12, name='save_tour'),
  path('fetch_and_save_tours/',views.fetch_and_save_tours,name='fetch_and_save_tours'),
  path('save_tours_to_db/',views.save_tours_to_db, name="save_tours_to_db"),
  path('recommend-course/', views.recommend_course_view, name='recommend-course'),
  # path('recommend-group-course/', views.recommend_group_course_view, name='recommend-group-course'),
  path('random_tour/', views.random_tour, name='random-tour'),
  path('routes_healing/<int:areacode>/<int:route_pk>/', views.routes_healing, name='routes_healing'),
  path('routes_activity/<int:areacode>/<int:route_pk>/', views.routes_activity, name='routes_activity'),
  path('routes_exhibit/<int:areacode>/<int:route_pk>/', views.routes_exhibit, name='routes_exhibit'),
  path('routes_food/<int:areacode>/<int:route_pk>/', views.routes_food, name='routes_food'),
  path('routes_people/<int:areacode>/<int:route_pk>/', views.routes_people, name='routes_people'),
  path('routes_experience/<int:areacode>/<int:route_pk>/', views.routes_experience, name='routes_experience'),
  path('routes_influencer/<int:areacode>/<int:route_pk>/', views.routes_influencer, name='routes_influencer'),
  path('routes_relax/<int:areacode>/<int:route_pk>/', views.routes_relax, name='routes_relax'),
]