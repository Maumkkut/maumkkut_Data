def get_tour_courses(character_type):
    if character_type == "힐링형 감자":
        categories = ["A0101", "A0201", "A0202", "A0303"]
    elif character_type == "액티비티형 옥수수":
        categories = ["A0301", "A0305", "A0202"]
    elif character_type == "관람형 배추":
        categories = ["A0201", "A0203", "A0205", "A0206"]
    elif character_type == "미식형 황태":
        categories = ["A0502", "A0401", "A0203", "A0204"]
    elif character_type == "사람형 쌀알":
        categories = ["A0101", "A0202", "A0203", "A0206", "A0302", "A0303"]
    elif character_type == "체험형 인삼":
        categories = ["A0203", "A0202", "A0302", "A0303", "A0305"]
    elif character_type == "인플루언서형 복숭아":
        categories = ["A0101", "A0202", "A0203", "A0205", "A0206"]
    elif character_type == "나무늘보형 순두부":
        categories = ["A0201", "A0202", "A0203", "A0502"]
    return categories

def filter_courses_by_distance(courses, base_location, max_distance=1):
    filtered_courses = []
    for course in courses:
        distance = geodesic((base_location.mapy, base_location.mapx), (course.mapy, course.mapx)).km
        if distance <= max_distance:
            filtered_courses.append(course)
    return filtered_courses

def recommend_course_view(request):
    if request.method == 'POST':
        region = request.POST.get('region')
        user_id = request.POST.get('user_id')
        
        try:
            user_preferences = UserPreferences.objects.get(user_id=user_id)
        except UserPreferences.DoesNotExist:
            return HttpResponseBadRequest("사용자의 중요도 정보가 없습니다.")
        
        travel_character = user_preferences.travel_character
        relaxation = user_preferences.relaxation
        
        categories = get_tour_courses(travel_character)
        
        base_location = Tours.objects.filter(region=region).first()
        if not base_location:
            return HttpResponseBadRequest("해당 지역에 대한 정보가 없습니다.")
        
        tours = Tours.objects.filter(cat2__in=categories, region=region)
        filtered_courses = filter_courses_by_distance(tours, base_location)

        if relaxation <= 2:
            result = filtered_courses[:6]
        elif relaxation == 3:
            result = filtered_courses[:5]
        else:
            result = filtered_courses[:4]

        return render(request, 'recommend_course.html', {'result': result})
    return render(request, 'recommend_course.html')