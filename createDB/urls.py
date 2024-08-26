from django.urls import path
from . import views

urlpatterns = [
  # path('save-tour-12/', views.save_tour_12, name='save_tour'),
  # path('fetch_and_save_tours/',views.fetch_and_save_tours,name='fetch_and_save_tours'),
  # path('save_tours_to_db/',views.save_tours_to_db, name="save_tours_to_db"),
  # path('recommend-course/', views.recommend_course_view, name='recommend-course'),
  # path('recommend-group-course/', views.recommend_group_course_view, name='recommend-group-course'),
  # 데이터 저장 urls
  # path('random_tour/', views.random_tour, name='random-tour'),
  path('routes_healing/<int:areacode>/<int:route_pk>/', views.routes_healing, name='routes_healing'),
  path('routes_activity/<int:areacode>/<int:route_pk>/', views.routes_activity, name='routes_activity'),
  path('routes_exhibit/<int:areacode>/<int:route_pk>/', views.routes_exhibit, name='routes_exhibit'),
  path('routes_food/<int:areacode>/<int:route_pk>/', views.routes_food, name='routes_food'),
  path('routes_people/<int:areacode>/<int:route_pk>/', views.routes_people, name='routes_people'),
  path('routes_experience/<int:areacode>/<int:route_pk>/', views.routes_experience, name='routes_experience'),
  path('routes_influencer/<int:areacode>/<int:route_pk>/', views.routes_influencer, name='routes_influencer'),
  path('routes_relax/<int:areacode>/<int:route_pk>/', views.routes_relax, name='routes_relax'),
  # 랜덤 관광지 데이터 조회 urls
  path('get_tours_by_area/<int:areacode>/', views.get_tours_by_area, name='get_tours_by_area'),
  path('get_tours_by_tour_type/<int:areacode>/<str:tour_type>/', views.get_tours_by_tour_type, name='get_tours_by_tour_type'),
  # 루트 데이터 조회 urls
  path('get_routes_data_by_route/<int:route_pk>/', views.get_routes_data_by_route, name='get_routes_data_by_route'),
  path('get_routes_by_route_area/<int:areacode>/', views.get_routes_by_route_area, name='get_routes_by_route_area'),
  path('get_routes_by_tour_type/<str:tour_type>/', views.get_routes_by_tour_type, name='get_routes_by_tour_type'),
  path('get_routes_by_tour_type_area/<int:areacode>/<str:tour_type>/', views.get_routes_by_tour_type_area, name='get_routes_by_tour_type_area')
]