from django.db import models
from django.forms import CharField
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class schedules(models.Model):
    title = models.CharField(max_length=50)

class streamer(models.Model):
    name = models.CharField(max_length=50)
    ch = models.TextField(null=True)

class UserInfo(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    

# class db_table(models.Model):
#     db_