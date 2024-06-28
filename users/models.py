from django.db import models
from django.contrib.auth.models import AbstractUser
from createDB.models import Routes

# Create your models here.
class User(AbstractUser):
    user_tour_type = models.TextField(null=True)
    user_healing = models.IntegerField(null=True)
    user_relax = models.IntegerField(null=True)
    user_nature = models.IntegerField(null=True)
    user_exhibit = models.IntegerField(null=True)
    user_food = models.IntegerField(null=True)
    user_adventure = models.IntegerField(null=True)
    user_people = models.IntegerField(null=True)
    user_shopping = models.IntegerField(null=True)
    user_photo = models.IntegerField(null=True)
    route = models.ForeignKey(Routes, on_delete=models.SET_NULL, null=True)


