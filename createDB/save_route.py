from .models import Groups, Group_Members, Tours, Routes_plan, Tour_plan_data
import json
import random
from django.core import serializers
from .filter_name import filter_type

def random_route(areacode, route_pk, tour_type):
    tour_data = filter_type(areacode, tour_type)
    random_tour_data = random.sample(list(tour_data), min(len(tour_data), 5))
    routes_plan = Routes_plan.objects.get(pk=route_pk)
    tour_seq = 1
    
    for tour in random_tour_data:
        Tour_plan_data.objects.create(
            tour=tour,
            route=routes_plan,
            tour_seq=tour_seq
        )
        tour_seq += 1
    random_data_json = json.loads(serializers.serialize('json', random_tour_data))
    return random_data_json