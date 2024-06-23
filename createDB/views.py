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