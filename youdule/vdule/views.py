from urllib import response
import requests
from django.shortcuts import redirect, render
import json
from django.conf import settings
from vdule.forms import UserForm
from .models import schedules, streamer
from .forms import Form
from .search_channel_id import search_channel_ids

# Create your views here.
def top(request):
    streamers = streamer.objects.all()
    
    return render(request, 'top.html', {'streamers':streamers})


def signup(request):
    post = streamer.objects.all()
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.post = post
            user.save()

    return render(request, 'signup.html', {"post": post})


def index(request):
    if request.method == "POST":
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        videos_url = 'https://www.googleapis.com/youtube/v3/videos'

        result_name = request.POST.get("name")
        channel_id = search_channel_ids(result_name)
        
        params = {
            'part' : 'snippet',
            'key' : settings.DEVELOPER_KEY,
            'maxResults' : 1,
            'channelId' : channel_id,
            'eventType' : 'upcoming',
            'type' : 'video',
            'order' : 'date'
        }

        r = requests.get(search_url, params=params)
        r = r.json()

        title = r["items"][0]["snippet"]["title"]
        thumbnail = r["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        video_id = r["items"][0]["id"]["videoId"]

        params1 = {
            'part' : 'liveStreamingDetails',
            'key' : settings.DEVELOPER_KEY,
            'id' : r["items"][0]["id"]["videoId"],
        }

        r = requests.get(videos_url, params=params1)
        date = r.json()

        date = date["items"][0]["liveStreamingDetails"]["scheduledStartTime"]

        return render(request, 'index.html', {'date':date, 'title':title, 'thumbnail':thumbnail, 'video_id':video_id})
    
    else:
        return render(request, 'index.html')
