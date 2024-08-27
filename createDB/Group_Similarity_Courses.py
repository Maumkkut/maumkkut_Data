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
from sklearn.feature_extraction.text import CountVectorizer
  
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

# 중요도를 리스트 형태로 가져오는 함수
def get_importance_list(user):
    importance_list = []
    importance_mapping = {
        '힐링': user.user_healing,
        '여유로움': user.user_relax,
        '자연': user.user_nature,
        '관람': user.user_exhibit,
        '음식점': user.user_food,
        '모험': user.user_adventure,
        '사람 많은 곳': user.user_people,
        '쇼핑': user.user_shopping,
        '사진 촬영': user.user_photo,
    }
    
    for key, value in importance_mapping.items():
        importance_list.extend([key] * value)
    
    return importance_list

# 코사인 유사도 계산
def calculate_cosine_similarity(group1, group2):
    vectorizer = CountVectorizer().fit_transform([' '.join(group1), ' '.join(group2)])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0][1]

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
    current_group_id = request.GET.get('group_id')

    # 현재 그룹의 구성원들의 중요도 리스트를 가져옴
    group_members = Group_Members.objects.filter(group_id=current_group_id)
    current_group_preferences = [get_importance_list(member.users) for member in group_members]

    if not current_group_preferences:
        return JsonResponse({"error": "현재 그룹에 구성원이 없습니다."}, status=400)

    # 단어 빈도를 반영하여 리스트 생성
    current_group_weighted_list = sum(current_group_preferences, [])

    # 다른 그룹들의 데이터 가져오기
    groups_data = []
    all_groups = Groups.objects.exclude(id=current_group_id)
    for group in all_groups:
        group_members = Group_Members.objects.filter(group_id=group.id)
        group_preferences = [get_importance_list(member.users) for member in group_members]
        if group_preferences:
            group_weighted_list = sum(group_preferences, [])
            groups_data.append({'id': group.id, 'preferences': group_weighted_list})

    # 가장 유사한 그룹 찾기
    similar_group = find_similar_group(current_group_weighted_list, groups_data)
    if not similar_group:
        return JsonResponse({"error": "유사한 그룹을 찾을 수 없습니다."}, status=400)

    # 유사한 그룹의 여행 코스 조회
    similar_group_id = similar_group['id']
    similar_group_routes = list(Routes_plan.objects.filter(group_id=similar_group_id).values())

    return JsonResponse({
        "message": "유사한 그룹의 여행 유형이 제공되었습니다.",
        "similar_group_id": similar_group_id,
        "similar_group_routes": similar_group_routes
    }, status=200)