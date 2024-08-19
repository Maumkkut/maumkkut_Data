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

###########################################################################################################
# 관광데이터 저장                                                  
###########################################################################################################

@api_view(['GET'])
def fetch_and_save_tours(request):
  URL = BASE_URL
  print('API_KEY:', api_key)
  params = {
    'serviceKey': api_key,
    "areaCode": "32",  # 강원도 코드
    'numOfRows': 1000,
    'pageNo': 6,
    'MobileOS': 'ETC',
    'MobileApp': 'TestApp',
    '_type': 'json'
  }
  response = requests.get(URL, params=params)
  print(response)
  response.raise_for_status()  # HTTP 오류가 발생했는지 확인
  print("Response status code:", response.status_code)
  print("Response text:", response.text)
  response = response.json()
  tour_data = response.get("response").get("body").get("items").get("item")

  if tour_data:
    save_tours_to_db(tour_data)
    return Response({"message": "데이터 저장 완료!"}, status=status.HTTP_201_CREATED)
  else:
    return Response({"error": "저장할 데이터가 없습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
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
    #   return JsonResponse({"message": "데이터 저장 완료!"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def random_tour(request):
    tour_data = Tours.objects.all()
    random_tour_data = random.sample(list(tour_data), min(len(tour_data), 5))
    random_data_json = json.loads(serializers.serialize('json', random_tour_data))
    return JsonResponse({'result': random_data_json})

@api_view(['GET'])
def routes_healing(request, areacode):
    tour_data = Tours.objects.filter(sigungucode=areacode)
    random_tour_data = random.sample(list(tour_data), min(len(tour_data), 5))
    random_data_json = json.loads(serializers.serialize('json', random_tour_data))
    return JsonResponse({'result': random_data_json})



###########################################################################################################
# 여행 캐릭터 유형                                                       
###########################################################################################################

def recommend_character(importance_list):
    # 캐릭터 목록을 정의 (각 캐릭터의 이름, 키워드 중요도, 설명)
    characters = [
        {
            "name": "힐링형 감자",
            "keywords": {"힐링": 5, "여유로움": 5, "자연": 5, "관람": 2, "음식점": 1, "모험": 1, "액티비티":1,"사람 많은 곳": 1, "쇼핑": 1, "사진 촬영": 2},
            "description": "조용하고 평화로운 환경을 선호, 주로 힐링을 목적으로 한 여행을 즐김"
        },
        {
            "name": "액티비티형 옥수수",
            "keywords": {"힐링": 1, "여유로움": 2, "자연": 4, "관람": 2, "음식점": 3, "모험": 5, "액티비티":5, "사람 많은 곳": 5, "쇼핑": 2, "사진 촬영": 4},
            "description": "모험과 활동적인 여행을 즐김, 다양한 액티비티 체험을 선호"
        },
        {
            "name": "관람형 배추",
            "keywords": {"힐링": 2, "여유로움": 3, "자연": 3, "관람": 5, "음식점": 3, "모험": 2, "액티비티":2, "사람 많은 곳": 2, "쇼핑": 3, "사진 촬영": 4},
            "description": "문화와 역사에 관심이 많아 박물관, 미술관 등을 자주 방문"
        },
        {
            "name": "미식형 황태",
            "keywords": {"힐링": 2, "여유로움": 4, "자연": 2, "관람": 3, "음식점": 5, "모험": 2, "액티비티":3,"사람 많은 곳": 4, "쇼핑": 4, "사진 촬영": 3},
            "description": "맛집 탐방과 음식을 즐기는 여행을 선호"
        },
        {
            "name": "사람좋아 쌀알",
            "keywords": {"힐링": 1, "여유로움": 2, "자연": 4, "관람": 2, "음식점": 3, "모험": 3, "액티비티":4,"사람 많은 곳": 5, "쇼핑": 4, "사진 촬영": 4},
            "description": "사람들이 많이 모이는 곳을 선호하고 활기찬 분위기를 즐김"
        },
        {
            "name": "도전형 인삼",
            "keywords": {"힐링": 2, "여유로움": 3, "자연": 5, "관람": 3, "음식점": 3, "모험": 5, "액티비티":5, "사람 많은 곳": 2, "쇼핑": 2, "사진 촬영": 4},
            "description": "새로운 시도를 즐기며 끊임없이 도전하는 여행을 선호"
        },
        {
            "name": "인플루언서형 복숭아",
            "keywords": {"힐링": 1, "여유로움": 2, "자연": 3, "관람": 3, "음식점": 4, "모험": 3, "액티비티":3, "사람 많은 곳": 5, "쇼핑": 5, "사진 촬영": 4},
            "description": "핫한 장소를 찾아다니며, 새로운 트렌드를 즐기고 공유"
        },
        {
            "name": "나무늘보형 순두부",
            "keywords": {"힐링": 4, "여유로움": 5, "자연": 3, "관람": 2, "음식점": 3, "모험": 1, "액티비티":1, "사람 많은 곳": 1, "쇼핑": 1, "사진 촬영": 2},
            "description": "일정에 구애받지 않고 여유로운 여행을 선호"
        }
    ]


    # 키워드 목록
    keywords = [
        "힐링", "여유로움", "자연", "관람", "음식점", "모험","액티비티","많은", "쇼핑", "사진 촬영"
    ]

    # 입력된 중요도를 choices 딕셔너리에 매핑
    choices = {keywords[i]: importance_list[i] for i in range(len(keywords))}

    best_match = None
    best_score = float('-inf')

    # 각 캐릭터의 점수를 계산
    for character in characters:
        # 캐릭터의 각 키워드 가중치와 사용자의 중요도를 곱한 값을 합산하여 점수 계산
        score = sum(choices.get(key, 0) * character["keywords"].get(key, 0) for key in choices)
        # 가장 높은 점수를 받은 캐릭터를 best_match로 설정
        if score > best_score:
            best_match = character
            best_score = score

    return best_match['name'], best_match['description']



# 예시 입력 리스트
importance_list = [5, 3, 4, 2, 1, 4, 3, 5, 2, 1]  # 사용자 입력 리스트

# 함수 호출 및 결과 출력
result = recommend_character(importance_list)
print(result)




###########################################################################################################
# 여행지 코스 추천                                                          
###########################################################################################################
# 공통                                                    
###########################################################################################################
region_codes = {
    "강릉시": 1,
    "고성군": 2,
    "동해시": 3,
    "삼척시": 4,
    "속초시": 5,
    "양구군": 6,
    "양양군": 7,
    "영월군": 8,
    "원주시": 9,
    "인제군": 10
}

def expand_cat3_ranges(cat3_ranges):
    expanded_cat3 = []
    for cat3_range in cat3_ranges:
        start, end = cat3_range.split(' ~ ')
        start_prefix = start[:-2]
        start_suffix = int(start[-2:])
        end_suffix = int(end[-2:])
        
        for i in range(start_suffix, end_suffix + 1):
            expanded_cat3.append(f"{start_prefix}{i:02d}")
    
    return expanded_cat3



def get_tour_courses(character_type):
    character_courses = {
        "힐링형 감자": {
            'type_ids': [12, 14, 32],
            'cat3_ranges': ['A01010100 ~ A01020200', 'A02010800 ~ A02010800', 'A02020300 ~ A02020800', 'A03030500 ~ A03030600'],
            'cat2': ['A0101', 'A0201', 'A0202', 'A0303']
        },
        "액티비티형 옥수수": {
            'type_ids': [28, 12, 25],
            'cat3_ranges': ['A03010200 ~ A03050100', 'A02020400 ~ A02020500'],
            'cat2': ['A0301', 'A0305', 'A0202']
        },
        "관람형 배추": {
            'type_ids': [14, 12, 25],
            'cat3_ranges': ['A02010100 ~ A02011000', 'A02030200 ~ A02030300', 'A02050200 ~ A02050200', 'A02060100 ~ A02060500', 'A04010700 ~ A04010700'],
            'cat2': ['A0201', 'A0203', 'A0205', 'A0206', 'A0401']
        },
        "미식형 황태": {
            'type_ids': [39, 38, 12],
            'cat3_ranges': ['A05020700 ~ A05020900', 'A04010100 ~ A04010200', 'A02030100 ~ A02030100', 'A02040600 ~ A02040600'],
            'cat2': ['A0502', 'A0401', 'A0203', 'A0204']
        },
        "사람좋아 쌀알": {
            'type_ids': [15, 12, 14],
            'cat3_ranges': ['A01011200 ~ A01011200', 'A02020400 ~ A02020800', 'A02030600 ~ A02030600', 'A02060400 ~ A02060400', 'A03021200 ~ A03021400', 'A03030800 ~ A03030800'],
            'cat2': ['A0101', 'A0202', 'A0203', 'A0206', 'A0302', 'A0303']
        },
        "도전형 인삼": {
            'type_ids': [25, 28, 12],
            'cat3_ranges': ['A02030100 ~ A02030400', 'A02020200 ~ A02020600', 'A03021800 ~ A03022400', 'A03030200 ~ A03030400', 'A03040300 ~ A03040400'],
            'cat2': ['A0203', 'A0202', 'A0302', 'A0303', 'A0305']
        },
        "인플루언서형 복숭아": {
            'type_ids': [15, 14, 12],
            'cat3_ranges': ['A01011200 ~ A01011200', 'A02020800 ~ A02020800', 'A02030600 ~ A02030600', 'A02050200 ~ A02050600', 'A02060100 ~ A02060500'],
            'cat2': ['A0101', 'A0202', 'A0203', 'A0205', 'A0206']
        },
        "나무늘보형 순두부": {
            'type_ids': [32, 12, 39],
            'cat3_ranges': ['A02010800 ~ A02010800', 'A02020300 ~ A02020600', 'A05020900 ~ A05020900'],
            'cat2': ['A0201', 'A0202', 'A0203', 'A0502']
        }
    }
    
    course_info = character_courses.get(character_type, None)
    if course_info:
        course_info['cat3'] = expand_cat3_ranges(course_info['cat3_ranges'])
    return course_info

# 소분류 우선 만약 소분류로 했을때 결과가 없으면 중분류까지 감
def filter_courses_by_preference(tour_courses, cat3_list, cat2_list):
    # 소분류 코드(cat3)로 필터링
    filtered_courses = [course for course in tour_courses if course.cat3 in cat3_list]
    # 소분류 코드로 필터링된 결과가 없으면 중분류 코드(cat2)로 필터링
    if not filtered_courses:
        filtered_courses = [course for course in tour_courses if course.cat2 in cat2_list]
    return filtered_courses


# 거리 계산 - 코스 추천시 코스별 거리가 멀면 안되기에
def filter_courses_by_distance(courses, base_location, max_distance=1.0):
    filtered_courses = []
    for course in courses:
        distance = geodesic((base_location.mapy, base_location.mapx), (course.mapy, course.mapx)).km
        if distance <= max_distance:
            filtered_courses.append(course)
    return filtered_courses


# 행사나 이벤트와 같이 종료 조건이 있다면 해당 날에 가능한지 여부파악
def filter_ongoing_events(courses):
    ongoing_courses = []
    today = datetime.today().date()
    for course in courses:
        if not course.eventenddate or course.eventenddate.date() >= today:
            ongoing_courses.append(course)
    return ongoing_courses


# 계절에 맞는 추천인지 확인
def filter_seasonal_courses(courses):
    seasonal_courses = []
    current_month = datetime.now().month
    for course in courses:
        # 눈썰매장, 스키/스노보드
        if course.cat3 in ["A03021200", "A03021400"] and (current_month in [12, 1, 2, 3]):
            seasonal_courses.append(course)
        # 수상 스포츠
        elif course.cat2 == "A0303" and (current_month in [6, 7, 8, 9]):
            seasonal_courses.append(course)
        else:
            seasonal_courses.append(course)
    return seasonal_courses


# 아침, 점심, 저녁대 별로 다르게 검색
def filter_courses_by_time(courses, time_of_day):
    time_filtered_courses = []
    for course in courses:
        if time_of_day == "morning" and course.type_id in [12, 14, 15, 28]:  # 아침: 관광지, 문화시설, 행사/공연/축제, 레포츠,
            time_filtered_courses.append(course)
        elif time_of_day == "afternoon" and course.type_id in [12, 14, 15, 28]:  # 점심: 관광지, 문화시설, 행사/공연/축제, 레포츠,
            time_filtered_courses.append(course)
        elif time_of_day == "evening" and course.type_id in [12, 38]:  # 저녁: 관광지,쇼핑
            time_filtered_courses.append(course)
    return time_filtered_courses


# 여유로움의 중요도에 따른 코스 개수 변경
def build_course_pattern(courses, food_courses, relaxation, food_importance, max_distance=1.0):
    pattern = []
    used_courses = set()
    
    if relaxation <= 2:
        course_count = 6
    elif relaxation == 3:
        course_count = 5
    else:
        course_count = 4

    selected_courses = courses[:course_count]
    
    current_location = selected_courses[0] if selected_courses else None

    for i in range(len(selected_courses) - 1):
        pattern.append(selected_courses[i])
        filtered_food_courses = filter_courses_by_distance(food_courses, selected_courses[i], max_distance)
        if filtered_food_courses:
            pattern.append(filtered_food_courses[0])  # 가장 가까운 음식점 추가
        current_location = selected_courses[i]

    pattern.append(selected_courses[-1])  # 마지막 놀거리 추가

    return pattern


###########################################################################################################
# 개인
########################################################################################################### 

@csrf_exempt
def recommend_course_view(request):
    importance_list = [5, 3, 4, 2, 1, 4, 3, 5, 2, 1]  # 중요도 리스트
    region = "강릉시"  # 지역

    # 유저 캐릭터가 "나무늘보형 순두부"로 지정된 경우를 가정
    user_preferences = {
        "travel_character": "나무늘보형 순두부",
        "relaxation": 4,
        "food_importance": 2
    }

    travel_character = user_preferences["travel_character"]
    relaxation = user_preferences["relaxation"]
    food_importance = user_preferences["food_importance"]
    
    course_info = get_tour_courses(travel_character)
    type_ids = course_info['type_ids']
    cat3_list = course_info['cat3']
    cat2_list = course_info['cat2']
    
    sigungucode = region_codes.get(region)
    if not sigungucode:
        return JsonResponse({"error": "해당 지역에 대한 정보가 없습니다."}, status=400)
    
    # 놀거리 데이터 가져오기
    tour_courses = list(Tours.objects.filter(type_id__in=type_ids, sigungucode=sigungucode))
    if not tour_courses:
        return JsonResponse({"error": "해당 지역에 대한 정보가 없습니다."}, status=400)
    
    # 종료된 행사/이벤트 제외
    tour_courses = filter_ongoing_events(tour_courses)
    
    # 계절에 맞는 코스 필터링
    tour_courses = filter_seasonal_courses(tour_courses)
    
    # 캐릭터 취향에 맞는 코스 필터링
    tour_courses = filter_courses_by_preference(tour_courses, cat3_list, cat2_list)
    
    # 시간대에 맞는 코스 필터링
    morning_courses = filter_courses_by_time(tour_courses, "morning")
    afternoon_courses = filter_courses_by_time(tour_courses, "afternoon")
    evening_courses = filter_courses_by_time(tour_courses, "evening")
    tour_courses = morning_courses + afternoon_courses + evening_courses
    
    # 음식점 데이터 가져오기
    food_courses = list(Tours.objects.filter(type_id=39, sigungucode=sigungucode))
    if not food_courses:
        return JsonResponse({"error": "해당 지역에 음식점 정보가 없습니다."}, status=400)
    
    # 디버깅 정보 출력
    print(f"Tours: {tour_courses}")
    print(f"Foods: {food_courses}")

    result = build_course_pattern(tour_courses, food_courses, relaxation, food_importance)


    # 최종 추천 코스 출력
    for course in result:
        print(f"추천 코스: {course.title} ({course.addr1})")

    # Tours 객체를 딕셔너리로 변환
    tour_courses_list = [{"title": tour.title, "addr1": tour.addr1, "mapx": tour.mapx, "mapy": tour.mapy} for tour in tour_courses]
    food_courses_list = [{"title": food.title, "addr1": food.addr1, "mapx": food.mapx, "mapy": food.mapy} for food in food_courses]
    result_list = [{"title": course.title, "addr1": course.addr1, "mapx": course.mapx, "mapy": course.mapy} for course in result]

    return JsonResponse({
        "message": "추천 코스가 콘솔에 출력되었습니다.",
        "tour_courses": tour_courses_list,
        "food_courses": food_courses_list,
        "filtered_courses": result_list
    }, status=200)


                                                         
###########################################################################################################
# 단체                                                 
###########################################################################################################

# 중요도를 기반으로 가중치 리스트 생성
def create_weighted_list(preferences):
    weighted_list = []
    keywords = [
        "힐링", "여유로움", "자연", "관람", "음식점", "모험", "액티비티", "사람 많은 곳", "쇼핑", "사진 촬영"
    ]
    for pref in preferences:
        for i, weight in enumerate(pref):
            weighted_list.extend([keywords[i]] * weight)
    return weighted_list

# 코사인 유사도 계산
def calculate_cosine_similarity(group1, group2):
    group1_vector = np.array([group1])
    group2_vector = np.array([group2])
    return cosine_similarity(group1_vector, group2_vector)[0][0]

# 유사한 그룹 찾기
def find_similar_group(current_group_preferences, groups_data):
    max_similarity = float('-inf')
    most_similar_group = None

    for group_data in groups_data:
        group_preferences = group_data['preferences']
        similarity = calculate_cosine_similarity(current_group_preferences, group_preferences)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_group = group_data

    return most_similar_group

@csrf_exempt
def recommend_similar_group_view(request):
    group_preferences = [
        [5, 3, 4, 2, 1, 4, 3, 5, 2, 1],
        [4, 4, 3, 3, 2, 5, 4, 4, 3, 2],
        [5, 2, 4, 3, 1, 3, 4, 5, 2, 1]
    ]
    region = "강릉시"

    current_group_weighted_list = create_weighted_list(group_preferences)
    print(f"Current Group Weighted List: {current_group_weighted_list}")

    groups_data = list(Groups.objects.filter(region=region).values('id', 'preferences'))
    for group_data in groups_data:
        group_data['preferences'] = create_weighted_list(list(Group_Members.objects.filter(group_id=group_data['id']).values_list('importance_list', flat=True)))

    similar_group = find_similar_group(current_group_weighted_list, groups_data)
    if not similar_group:
        return JsonResponse({"error": "유사한 그룹을 찾을 수 없습니다."}, status=400)

    similar_group_id = similar_group['id']
    similar_group_routes = list(Routes.objects.filter(group_id=similar_group_id).values())

    return JsonResponse({
        "message": "유사한 그룹의 여행 유형이 제공되었습니다.",
        "similar_group_id": similar_group_id,
        "similar_group_routes": similar_group_routes
    }, status=200)




##################################################################################
# 기존
##################################################################################


# # 각 단체 구성원의 중요도 리스트를 받아 중앙값을 계산
# def calculate_group_median(preferences):
#     preferences_array = np.array(preferences)
#     return np.median(preferences_array, axis=0).tolist()


# def recommend_group_course_view(request):
#     # 예시 단체 구성원 중요도 리스트
#     group_preferences = [
#         {"user_id": 1, "travel_character": "힐링형 감자"},
#         {"user_id": 2, "travel_character": "힐링형 감자"},
#         {"user_id": 3, "travel_character": "도전형 인삼"}
#     ]
#     region = "강릉시"  # 지역

#     # 단체의 중앙값 계산
#     group_median_preferences = calculate_group_median(group_preferences)
#     print(f"Group Median Preferences: {group_median_preferences}")

#     # 중앙값을 바탕으로 유저 캐릭터 결정
#     character_name, character_description = recommend_character(group_median_preferences)
#     print(f"Determined Character: {character_name}, Description: {character_description}")

#     # 유저 캐릭터 설정
#     user_preferences = {
#         "travel_character": character_name,
#         "relaxation": int(group_median_preferences[1]),  # 여유로움 인덱스: 1번
#         "food_importance": int(group_median_preferences[4])  # 음식점 인덱스: 4번
#     }

#     travel_character = user_preferences["travel_character"]
#     relaxation = user_preferences["relaxation"]
#     food_importance = user_preferences["food_importance"]

#     # 캐릭터에 맞는 코스 정보 가져오기
#     course_info = get_tour_courses(travel_character)
#     if not course_info:
#         return JsonResponse({"error": "해당 캐릭터에 대한 코스 정보가 없습니다."}, status=400)

#     type_ids = course_info['type_ids']
#     cat3_list = course_info['cat3']
#     cat2_list = course_info['cat2']

#     sigungucode = region_codes.get(region)
#     if not sigungucode:
#         return JsonResponse({"error": "해당 지역에 대한 정보가 없습니다."}, status=400)

#     # 놀거리 데이터 가져오기
#     tour_courses = list(Tours.objects.filter(type_id__in=type_ids, sigungucode=sigungucode))
#     if not tour_courses:
#         return JsonResponse({"error": "해당 지역에 대한 정보가 없습니다."}, status=400)

#     # 종료된 행사/이벤트 제외
#     tour_courses = filter_ongoing_events(tour_courses)

#     # 계절에 맞는 코스 필터링
#     tour_courses = filter_seasonal_courses(tour_courses)

#     # 캐릭터 취향에 맞는 코스 필터링
#     tour_courses = filter_courses_by_preference(tour_courses, cat3_list, cat2_list)

#     # 시간대에 맞는 코스 필터링
#     morning_courses = filter_courses_by_time(tour_courses, "morning")
#     afternoon_courses = filter_courses_by_time(tour_courses, "afternoon")
#     evening_courses = filter_courses_by_time(tour_courses, "evening")
#     tour_courses = morning_courses + afternoon_courses + evening_courses

#     # 음식점 데이터 가져오기
#     food_courses = list(Tours.objects.filter(type_id=39, sigungucode=sigungucode))
#     if not food_courses:
#         return JsonResponse({"error": "해당 지역에 음식점 정보가 없습니다."}, status=400)

#     # 디버깅 정보 출력
#     print(f"Tours: {tour_courses}")
#     print(f"Foods: {food_courses}")

#     result = build_course_pattern(tour_courses, food_courses, relaxation, food_importance)

#     # 최종 추천 코스 출력
#     for course in result:
#         print(f"추천 코스: {course.title} ({course.addr1})")

#     # Tours 객체를 딕셔너리로 변환
#     tour_courses_list = [{"title": tour.title, "addr1": tour.addr1, "mapx": tour.mapx, "mapy": tour.mapy} for tour in tour_courses]
#     food_courses_list = [{"title": food.title, "addr1": food.addr1, "mapx": food.mapx, "mapy": food.mapy} for food in food_courses]
#     result_list = [{"title": course.title, "addr1": course.addr1, "mapx": course.mapx, "mapy": course.mapy} for course in result]

#     return JsonResponse({
#         "message": "추천 코스가 콘솔에 출력되었습니다.",
#         "character": character_name,
#         "character_description": character_description,
#         "tour_courses": tour_courses_list,
#         "food_courses": food_courses_list,
#         "filtered_courses": result_list
#     }, status=200)