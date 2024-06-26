from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .serializers import TourSerializer
from .models import Groups, Group_Members, Tours, Routes
from django.shortcuts import get_object_or_404, get_list_or_404

# Create your views here.

api_key = settings.API_KEY
BASE_URL = 'https://apis.data.go.kr/B551011/KorService1/areaBasedList1'
 # ?serviceKey=api_key&contentTypeId=28&numOfRows=10&pageNo=1&MobileOS=ETC&MobileApp=TestApp&_type=json

@api_view(['GET'])
def save_tour_12(request):
  URL = BASE_URL
  params = {
    'serviceKey': api_key,
    'contentTypeId': 12,
    'numOfRows': 100, 
    'pageNo': 1, 
    'MobileOS': 'ETC',
    'MobileApp': 'TestApp',
    '_type': 'json'
  }
  response = requests.get(URL, params=params).json()
  tour_data = response.get("response").get("body").get("items").get("item")
  return Response(tour_data)



@api_view(['GET'])
def fetch_and_save_tours(request):
  URL = BASE_URL
  params = {
    'serviceKey': api_key,
    'contentTypeId': 12,
    'numOfRows': 1000,
    'pageNo': 1,
    'MobileOS': 'ETC',
    'MobileApp': 'TestApp',
    '_type': 'json'
  }
  response = requests.get(URL, params=params).json()
  tour_data = response.get("response").get("body").get("items").get("item")

  if tour_data:
    save_tours_to_db(tour_data)
    return Response({"message": "데이터 저장 완료!"}, status=status.HTTP_201_CREATED)
  else:
    return Response({"error": "저장할 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

def save_tours_to_db(tour_data):
  for tour in tour_data:
    # 중복 확인
    if not Tours.objects.filter(title=tour.get("title")).exists():
      tour_instance = Tours(
        id=tour.get("id"),
        sigungucode=tour.get("sigungucode", None),
        addr1=tour.get("addr1", ""),
        addr2=tour.get("addr2", ""),
        image=tour.get("firstimage", ""),
        cat1=tour.get("cat1", ""),
        cat2=tour.get("cat2", ""),
        cat3=tour.get("cat3", ""),
        type_id=tour.get("contenttypeid", None),
        mapx=tour.get("mapx", 0),
        mapy=tour.get("mapy", 0),
        title=tour.get("title", ""),
        zipcode=tour.get("zipcode") if tour.get("zipcode") else None,
        tel=tour.get("tel", ""),
        eventstartdate=tour.get("eventstartdate", None),
        eventenddate=tour.get("eventenddate", None)
      )
      tour_instance.save()

