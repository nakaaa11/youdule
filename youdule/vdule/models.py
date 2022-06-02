from django.db import models
from django.forms import CharField

# Create your models here.
class schedules(models.Model):
    title = models.CharField(max_length=50)

class streamer(models.Model):
    name = models.CharField(max_length=50)
    ch = models.TextField(null=True)

class UserInfo(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    