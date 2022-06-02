from django.contrib import admin
from .models import schedules, streamer

# Register your models here.
admin.site.register(schedules)
admin.site.register(streamer)