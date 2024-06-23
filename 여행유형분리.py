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
