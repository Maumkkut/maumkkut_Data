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