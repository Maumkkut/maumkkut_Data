from django.db import models
from django.contrib.auth.models import AbstractUser
from createDB.models import Tours

# Create your models here.
class User_info(AbstractUser):
    # user_id = models.ForeignKey
    user_age = models.IntegerField(null=True)
    user_type = models.TextField(null=True)
    user_healing = models.IntegerField(null=True)
    user_relax = models.IntegerField(null=True)
    user_nature = models.IntegerField(null=True)
    user_exhibit = models.IntegerField(null=True)
    user_food = models.IntegerField(null=True)
    user_adventure = models.IntegerField(null=True)
    user_people = models.IntegerField(null=True)
    user_shopping = models.IntegerField(null=True)
    user_photo = models.IntegerField(null=True)
    tour_like = models.ManyToManyField(Tours, symmetrical=False, related_name='liked_users')
    tour_dislike = models.ManyToManyField(Tours, symmetrical=False, related_name='disliked_users')


