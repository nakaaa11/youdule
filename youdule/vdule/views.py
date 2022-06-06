from datetime import timedelta
from pprint import pprint
from urllib import response
import requests
import json
from django.shortcuts import redirect, render
from django.conf import settings
from vdule.forms import UserForm
from .models import schedules, streamer
from .forms import Form
from .search_channel_id import search_channel_ids
from django.contrib.auth.decorators import login_required
import google_auth_oauthlib.flow
import google.oauth2.credentials
from .subscription import get_subscriptions

CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtubepartner-channel-audit']

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
        if result_name == "" :
            return render(request, 'index.html')
        else:
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

            try:
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

            except:
                return render(request, 'index.html')

    else:
        return render(request, 'index.html')


# @login_required
def need(request):
    first_name_list = ["ichiro", "hideki", "hideo"]
    second_name_list = ["suzuki", "matsui", "nomo"]
    l4 = []

    for i in range(len(first_name_list)):
        l3 = []
        l3.append(first_name_list[i])
        l3.append(second_name_list[i])
        l4.append(l3)

    print(l4)
    # temp_list = []
    # for i, _ in enumerate(first_name_list):
    #     temp_list.append({
    #         'first_name': first_name_list[i],
    #         'second_name': second_name_list[i],
    #     })

    return render(request, 'need.html', {"l4": l4})


def mypage(request):
    channel_ids = get_subscriptions()
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    videos_url = 'https://www.googleapis.com/youtube/v3/videos'

    titles = []
    thumbnails = []
    video_ids =[]
    dates = []

    for channelId in channel_ids:
        params = {
            'part' : 'snippet',
            'key' : settings.DEVELOPER_KEY,
            'maxResults' : 1,
            'channelId' : channelId,
            'eventType' : 'completed',
            'type' : 'video',
            'order' : 'date',
        }

        r = requests.get(search_url, params=params)
        r = r.json()

        if r["error"]["code"] == 403:
            print('The request cannot be completed because you have exceeded your <a href="/youtube/v3/getting-started#quota">quota</a>.')

        try:
            titles.append(r["items"][0]["snippet"]["title"])
            thumbnails.append(r["items"][0]["snippet"]["thumbnails"]["default"]["url"])
            video_ids.append(r["items"][0]["id"]["videoId"])

        except:
            print("error, break")
            break

    for video_id in video_ids:
        params1 = {
            'part' : 'liveStreamingDetails',
            'key' : settings.DEVELOPER_KEY,
            'id' : video_id,
        }

        r = requests.get(videos_url, params=params1)
        r = r.json()

        try:
            dates.append(r["items"][0]["liveStreamingDetails"]["scheduledStartTime"])
            dates = dates + timedelta(hours=9)

        except:
            print('error, break')
            break

    print("good")
    return render(request, 'mypage.html', {'dates':dates, 'titles':titles, 'thumbnails':thumbnails, 'video_ids':video_ids})