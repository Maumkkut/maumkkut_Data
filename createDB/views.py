from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .serializers import TourSerializer
from .models import Groups, Group_Members, Tours, Routes
from django.shortcuts import get_object_or_404, get_list_or_404
from geopy.distance import geodesic

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

############################################################################
# 관광데이터 저장                                                  
############################################################################

@api_view(['GET'])
def fetch_and_save_tours(request):
  URL = BASE_URL
  params = {
    'serviceKey': api_key,
    "areaCode": "32",  # 강원도 코드
    'numOfRows': 1000,
    'pageNo': 6,
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


############################################################################
# 여행 캐릭터 유형                                                       
############################################################################

def recommend_character(importance_list):
    # 캐릭터 목록을 정의 (각 캐릭터의 이름, 키워드 중요도, 설명)
    characters = [
        {
            "name": "힐링형 감자",
            "keywords": {"힐링": 5, "여유로움": 5, "자연": 5, "관람": 2, "음식점": 1, "모험": 1, "사람 많은 곳": 1, "쇼핑": 1, "사진 촬영": 2},
            "description": "조용하고 평화로운 환경을 선호, 주로 힐링을 목적으로 한 여행을 즐김"
        },
        {
            "name": "액티비티형 옥수수",
            "keywords": {"힐링": 1, "여유로움": 2, "자연": 4, "관람": 2, "음식점": 3, "모험": 5, "사람 많은 곳": 5, "쇼핑": 2, "사진 촬영": 4},
            "description": "모험과 활동적인 여행을 즐김, 다양한 액티비티 체험을 선호"
        },
        {
            "name": "관람형 배추",
            "keywords": {"힐링": 2, "여유로움": 3, "자연": 3, "관람": 5, "음식점": 3, "모험": 2, "사람 많은 곳": 2, "쇼핑": 3, "사진 촬영": 4},
            "description": "문화와 역사에 관심이 많아 박물관, 미술관 등을 자주 방문"
        },
        {
            "name": "미식형 황태",
            "keywords": {"힐링": 2, "여유로움": 4, "자연": 2, "관람": 3, "음식점": 5, "모험": 2, "사람 많은 곳": 4, "쇼핑": 4, "사진 촬영": 3},
            "description": "맛집 탐방과 음식을 즐기는 여행을 선호"
        },
        {
            "name": "사람좋아 쌀알",
            "keywords": {"힐링": 1, "여유로움": 2, "자연": 4, "관람": 2, "음식점": 3, "모험": 3, "사람 많은 곳": 5, "쇼핑": 4, "사진 촬영": 4},
            "description": "사람들이 많이 모이는 곳을 선호하고 활기찬 분위기를 즐김"
        },
        {
            "name": "도전형 인삼",
            "keywords": {"힐링": 2, "여유로움": 3, "자연": 5, "관람": 3, "음식점": 3, "모험": 5, "사람 많은 곳": 2, "쇼핑": 2, "사진 촬영": 4},
            "description": "새로운 시도를 즐기며 끊임없이 도전하는 여행을 선호"
        },
        {
            "name": "인플루언서형 복숭아",
            "keywords": {"힐링": 1, "여유로움": 2, "자연": 3, "관람": 3, "음식점": 4, "모험": 3, "사람 많은 곳": 5, "쇼핑": 5, "사진 촬영": 4},
            "description": "핫한 장소를 찾아다니며, 새로운 트렌드를 즐기고 공유"
        },
        {
            "name": "나무늘보형 순두부",
            "keywords": {"힐링": 4, "여유로움": 5, "자연": 3, "관람": 2, "음식점": 3, "모험": 1, "사람 많은 곳": 1, "쇼핑": 1, "사진 촬영": 2},
            "description": "일정에 구애받지 않고 여유로운 여행을 선호"
        }
    ]


    # 키워드 목록
    keywords = [
        "힐링", "액티비티", "자연", "관람", "음식점", "모험",
        "여유로움", "사람 많은 곳", "쇼핑", "사진 촬영"
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




############################################################################
# 여행지 코스 추천                                                          
############################################################################
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

def get_tour_courses(character_type):
    if character_type == "힐링형 감자":
        return {
            'type_ids': [12, 14, 32],
            'cat2': ['A0101', 'A0201', 'A0202', 'A0303']
        }
    elif character_type == "액티비티형 옥수수":
        return {
            'type_ids': [28, 12, 25],
            'cat2': ['A0301', 'A0305', 'A0202']
        }
    elif character_type == "관람형 배추":
        return {
            'type_ids': [14, 12, 25],
            'cat2': ['A0201', 'A0203', 'A0205', 'A0206', 'A0401']
        }
    elif character_type == "미식형 황태":
        return {
            'type_ids': [39, 38, 12],
            'cat2': ['A0502', 'A0401', 'A0203', 'A0204']
        }
    elif character_type == "사람형 쌀알":
        return {
            'type_ids': [15, 12, 14],
            'cat2': ['A0101', 'A0202', 'A0203', 'A0206', 'A0302', 'A0303']
        }
    elif character_type == "체험형 인삼":
        return {
            'type_ids': [25, 28, 12],
            'cat2': ['A0203', 'A0202', 'A0302', 'A0303', 'A0305']
        }
    elif character_type == "인플루언서형 복숭아":
        return {
            'type_ids': [15, 14, 12],
            'cat2': ['A0101', 'A0202', 'A0203', 'A0205', 'A0206']
        }
    elif character_type == "나무늘보형 순두부":
        return {
            'type_ids': [32, 12, 39],
            'cat2': ['A0201', 'A0202', 'A0203', 'A0502']
        }

# 거리 반영
def filter_courses_sequentially(courses, max_distance=1.0):
    filtered_courses = []
    if not courses:
        return filtered_courses
    
    current_location = courses[0]
    filtered_courses.append(current_location)
    
    for next_course in courses[1:]:
        distance = geodesic((current_location.mapy, current_location.mapx), (next_course.mapy, next_course.mapx)).km
        print(f"Course: {next_course.title}, Distance: {distance} km")  # 거리 디버깅 정보 출력
        if distance <= max_distance:
            filtered_courses.append(next_course)
            current_location = next_course
    
    return filtered_courses


# 코스 (관광 > 밥 > 관관...) - 여유도에 따라 다르게
def build_course_pattern(courses, food_courses, relaxation, food_importance, max_distance=1.0):
    pattern = []
    used_courses = set()
    
    if relaxation <= 2:
        course_count = 6
    elif relaxation == 3:
        course_count = 5
    else:
        course_count = 4

    current_location = None
    i = 0

    if food_importance >= 4:
        while len(pattern) < course_count:
            if len(pattern) % 2 == 0:  # 놀거리 추가
                for course in courses:
                    if course not in used_courses:
                        pattern.append(course)
                        used_courses.add(course)
                        break
            else:  # 음식점 추가
                for food in food_courses:
                    if food not in used_courses:
                        pattern.append(food)
                        used_courses.add(food)
                        break
            i += 1
    else:
        while len(pattern) < course_count:
            if len(pattern) % 2 == 0:  # 놀거리 추가
                for course in courses:
                    if course not in used_courses and (current_location is None or geodesic((current_location.mapy, current_location.mapx), (course.mapy, course.mapx)).km <= max_distance):
                        pattern.append(course)
                        used_courses.add(course)
                        current_location = course
                        break
            else:  # 음식점 추가
                for food in food_courses:
                    if food not in used_courses and (current_location is None or geodesic((current_location.mapy, current_location.mapx), (food.mapy, food.mapx)).km <= max_distance):
                        pattern.append(food)
                        used_courses.add(food)
                        current_location = food
                        break
            i += 1

    return pattern




@csrf_exempt
def recommend_course_view(request):
    importance_list = [5, 3, 4, 2, 1, 4, 3, 5, 2, 1]  # 중요도 리스트
    region = "강릉시"  # 지역

    # 유저 캐릭터가 "나무늘보형 순두부"로 지정된 경우를 가정
    user_preferences = {
        "travel_character": "나무늘보형 순두부",
        "relaxation": 4,
        "food_importance":2
    }

    travel_character = user_preferences["travel_character"]
    relaxation = user_preferences["relaxation"]
    food_importance = user_preferences["food_importance"]
    course_info = get_tour_courses(travel_character)
    type_ids = course_info['type_ids']
    cat2_list = course_info['cat2']
    
    sigungucode = region_codes.get(region)
    if not sigungucode:
        return JsonResponse({"error": "해당 지역에 대한 정보가 없습니다."}, status=400)
    
    # 놀거리 데이터 가져오기
    tour_courses = list(Tours.objects.filter(type_id__in=type_ids, sigungucode=sigungucode, cat2__in=cat2_list))
    if not tour_courses:
        return JsonResponse({"error": "해당 지역에 대한 정보가 없습니다."}, status=400)
    
    # 음식점 데이터 가져오기
    food_courses = list(Tours.objects.filter(type_id=39, sigungucode=sigungucode))
    if not food_courses:
        return JsonResponse({"error": "해당 지역에 음식점 정보가 없습니다."}, status=400)
    
    # 디버깅 정보 출력
    print(f"Tours: {tour_courses}")
    print(f"Foods: {food_courses}")

    filtered_tour_courses = filter_courses_sequentially(tour_courses)
    filtered_food_courses = filter_courses_sequentially(food_courses)
    print("음식점:",filtered_food_courses)
    print("놀거리:",filtered_tour_courses)

    result = build_course_pattern(filtered_tour_courses, filtered_food_courses, relaxation, food_importance)


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