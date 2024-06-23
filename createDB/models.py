from django.db import models
from django.conf import settings

# Create your models here.
class Groups(models.Model):
  users = models.ManyToManyField(
    settings.AUTH_USER_MODEL, related_name='joined_group', through='Group_Members'
    )
  people_num = models.IntegerField()
  tour_type = models.CharField(max_length=10, null=True)
  group_name = models.CharField(max_length=20)

# 지금 상황에서는 중개 테이블이 필요 없지만, 나중에 추가 정보 저장 가능성을 위해 제작
class Group_Members(models.Model):
  users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  group = models.ForeignKey(Groups, on_delete=models.CASCADE)

class Routes(models.Model):
  group = models.ForeignKey(Groups, on_delete=models.CASCADE)
  route_name = models.CharField(max_length=20)
