from django.urls import path
from . import views

urlpatterns = [
  # path('save-tour-12/', views.save_tour_12, name='save_tour'),
  # path('fetch_and_save_tours/',views.fetch_and_save_tours,name='fetch_and_save_tours'),
  # path('save_tours_to_db/',views.save_tours_to_db, name="save_tours_to_db"),
  # path('recommend-group-course/', views.recommend_group_course_view, name='recommend-group-course'),
  # 데이터 저장 urls
  path('save_random_route/<int:areacode>/<int:route_pk>/<str:tour_type>/', views.save_random_route, name='save_random_route'),
  # 랜덤 관광지 데이터 조회 urls
  path('get_tours_by_area/<int:areacode>/', views.get_tours_by_area, name='get_tours_by_area'),
  path('get_tours_by_tour_type/<int:areacode>/<str:tour_type>/', views.get_tours_by_tour_type, name='get_tours_by_tour_type'),
  # 루트 데이터 조회 urls
  path('get_routes_data_by_route/<int:route_pk>/', views.get_routes_data_by_route, name='get_routes_data_by_route'),
  path('get_routes_by_route_area/<int:areacode>/', views.get_routes_by_route_area, name='get_routes_by_route_area'),
  path('get_routes_by_tour_type/<str:tour_type>/', views.get_routes_by_tour_type, name='get_routes_by_tour_type'),
  path('get_routes_by_tour_type_area/<int:areacode>/<str:tour_type>/', views.get_routes_by_tour_type_area, name='get_routes_by_tour_type_area'),
  # 개인 여행 유형별 코스 추천
  path('recommend-course/', views.recommend_course_view, name='recommend-course'),
  # 비슷한 그룹 검색 및 코스 조회
  path('recommend_similar_group/', views.recommend_similar_group_view, name='recommend_similar_group'),
]