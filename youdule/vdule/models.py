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
    
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     gender = models.CharField(max_length=20, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     favorite_words = models.CharField(max_length=50, blank=True)
#     avatar = models.URLField(max_length=200, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()