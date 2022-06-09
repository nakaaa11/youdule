from django.contrib import admin
from .models import schedules, Streamer

# Register your models here.
admin.site.register(schedules)
admin.site.register(Streamer)