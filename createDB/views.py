from datetime import datetime
import numpy as np
from django.shortcuts import render
from django.conf import settings
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .serializers import TourSerializer
from .models import Groups, Group_Members, Tours, Routes_plan, Tour_plan_data
from django.shortcuts import get_object_or_404, get_list_or_404
from geopy.distance import geodesic
from sklearn.metrics.pairwise import cosine_similarity
import json
import random
from django.db.models import Q
from .random_route import random_area, random_tour_type
from .get_route_data import route_data_by_pk, route_data_by_area, route_data_by_tour_type, route_data_by_tour_type_area
from .save_route import random_route
from .Personalized_Type_Course import *
from .Group_Similarity_Courses import *
from sklearn.feature_extraction.text import CountVectorizer
# Create your views here.

api_key = settings.API_KEY
BASE_URL = 'https://apis.data.go.kr/B551011/KorService1/areaBasedList1'

###########################################################################################################
# 관광데이터 저장                                                  
###########################################################################################################

# @api_view(['GET'])
# def fetch_and_save_tours(request):
#   URL = BASE_URL
#   print('API_KEY:', api_key)
#   params = {
#     'serviceKey': api_key,
#     "areaCode": "32",  # 강원도 코드
#     'numOfRows': 1000,
#     'pageNo': 6,
#     'MobileOS': 'ETC',
#     'MobileApp': 'TestApp',
#     '_type': 'json'
#   }
#   response = requests.get(URL, params=params)
#   print(response)
#   response.raise_for_status()  # HTTP 오류가 발생했는지 확인
#   print("Response status code:", response.status_code)
#   print("Response text:", response.text)
#   response = response.json()
#   tour_data = response.get("response").get("body").get("items").get("item")

#   if tour_data:
#     save_tours_to_db(tour_data)
#     return Response({"message": "데이터 저장 완료!"}, status=status.HTTP_201_CREATED)
#   else:
#     return Response({"error": "저장할 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def save_tours_to_db(tour_data):
#   for tour in tour_data:
#     # 중복 확인
#     if not Tours.objects.filter(title=tour.get("title")).exists():
#       tour_instance = Tours(
#         id=tour.get("id"),
#         sigungucode=tour.get("sigungucode", None),
#         addr1=tour.get("addr1", ""),
#         addr2=tour.get("addr2", ""),
#         image=tour.get("firstimage", ""),
#         cat1=tour.get("cat1", ""),
#         cat2=tour.get("cat2", ""),
#         cat3=tour.get("cat3", ""),
#         type_id=tour.get("contenttypeid", None),
#         mapx=tour.get("mapx", 0),
#         mapy=tour.get("mapy", 0),
#         title=tour.get("title", ""),
#         zipcode=tour.get("zipcode") if tour.get("zipcode") else None,
#         tel=tour.get("tel", ""),
#         eventstartdate=tour.get("eventstartdate", None),
#         eventenddate=tour.get("eventenddate", None)
#       )
#       tour_instance.save()
#     #   return JsonResponse({"message": "데이터 저장 완료!"}, status=status.HTTP_201_CREATED)

##############################################################
# 관광지 유형별 루트 데이터 저장 함수
#############################################################################
@api_view(['GET'])
def save_random_route(request, areacode, route_pk, tour_type):
    return JsonResponse({'result': random_route(areacode, route_pk, tour_type)})

##################################################################################################
# 랜덤 관광지 추천받는 함수
##################################################################################

@api_view(['GET'])
def get_tours_by_area(request, areacode):
    return JsonResponse({'result': random_area(areacode)})

@api_view(['GET'])
def get_tours_by_tour_type(request, areacode, tour_type):
    return JsonResponse({'result': random_tour_type(areacode, tour_type)})


##########################################################################
# 관광지 루트 조회 함수
####################################################################################

@api_view(['GET'])
def get_routes_data_by_route(request, route_pk):
    return JsonResponse({'result': route_data_by_pk(route_pk)}, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@api_view(['GET'])
def get_routes_by_route_area(request, areacode):
    return JsonResponse({'result': route_data_by_area(areacode)}, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@api_view(['GET'])
def get_routes_by_tour_type(request, tour_type):
    return JsonResponse({'result': route_data_by_tour_type(tour_type)}, json_dumps_params={'ensure_ascii': False, 'indent': 4})

@api_view(['GET'])
def get_routes_by_tour_type_area(request, areacode, tour_type):
    return JsonResponse({'result': route_data_by_tour_type_area(areacode, tour_type)}, json_dumps_params={'ensure_ascii': False, 'indent': 4})

###########################################################################################################
# 여행 캐릭터 유형                                                     
###########################################################################################################

# print(recommend_course_view([1,3,4,2,5,3,1,4,2,5], "힐링형 감자","강릉"))