from datetime import datetime
import json
import os
import sys
from datetime import timedelta
from pprint import pprint
from turtle import st
from urllib import response
import google.oauth2.credentials
import google_auth_oauthlib.flow
import httplib2
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from vdule.forms import UserForm

from .forms import Form
from .models import Streamer
from .search_channel_id import search_channel_ids

import feedparser

# from .subscription import get_subscriptions

CLIENT_SECRETS_FILE = '/Users/nak/Desktop/python_lesson/app/youdule/client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtubepartner-channel-audit']

# Create your views here.
def top(request):
    streamers = Streamer.objects.all()
    
    return render(request, 'top.html', {'streamers':streamers})


def signup(request):
    post = Streamer.objects.all()
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
                'order' : 'date',
                'fields': 'items',
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
                    'fields': 'items'
                }

                r = requests.get(videos_url, params=params1)
                date = r.json()

                date = date["items"][0]["liveStreamingDetails"]["scheduledStartTime"]

                return render(request, 'index.html', {'date':date, 'title':title, 'thumbnail':thumbnail, 'video_id':video_id})

            except:
                return render(request, 'index.html')

    else:
        return render(request, 'index.html')


def mypage(request):
    CLIENT_SECRETS_FILE = "/Users/nak/Desktop/python_lesson/app/youdule/client_secrets.json"

  # This variable defines a message to display if the CLIENT_SECRETS_FILE is
  # missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the client_secrets.json file
    found at:%s

    with information from the API Console
    https://console.developers.google.com/

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__),CLIENT_SECRETS_FILE))

    # This OAuth 2.0 access scope allows for full read/write access to the
    # authenticated user's account.
    YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        message=MISSING_CLIENT_SECRETS_MESSAGE,
        scope=YOUTUBE_READ_WRITE_SCOPE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flags = argparser.parse_args([])
        credentials = run_flow(flow, storage, flags)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()))

    #自身のYouTubeのIDを取得
    r = youtube.channels().list(
        part="snippet",
        mine="True",
    ).execute()

    channel_id = r["items"][0]["id"]

    channel_ids = []
    channel_names = []
    #自身のYouTubeIDから登録チャンネルのリストを取得
    request = youtube.subscriptions().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        fields="nextPageToken, items/snippet",
    )

    while request:
        response = request.execute()
        channel_ids.extend(list(map(lambda item: item["snippet"]["resourceId"]["channelId"], response["items"])))
        channel_names.extend(list(map(lambda item: item["snippet"]["title"], response["items"])))
        request = youtube.subscriptions().list_next(request, response)

    lists = []

    videos_url = 'https://www.googleapis.com/youtube/v3/videos'

    for channelId in channel_ids:
        mls_rdf = (f'https://www.youtube.com/feeds/videos.xml?channel_id={channelId}')
        mls_dic = feedparser.parse(mls_rdf)

        video_id = mls_dic['entries'][0]['yt_videoid']
        title = mls_dic['entries'][0]['title']
        thumbnail = mls_dic['entries'][0]['media_thumbnail'][0]['url']
        author = mls_dic['entries'][0]['authors'][0]['name']

        if not Streamer.objects.filter(channel_id=channelId).exists():
            Streamer.objects.create(name=author, channel_id=channelId)

        params1 = {
            'part' : 'snippet',
            'key' : settings.DEVELOPER_KEY,
            'id' : video_id,
            'fields' : 'items/snippet/liveBroadcastContent'
        }

        res = requests.get(videos_url, params=params1)
        res = res.json()

        status = res['items'][0]['snippet']['liveBroadcastContent']

        if status == 'upcoming':    
            params1 = {
                'part' : 'liveStreamingDetails',
                'key' : settings.DEVELOPER_KEY,
                'id' : video_id,
                'fields' : 'items/liveStreamingDetails/scheduledStartTime'
            }

            res = requests.get(videos_url, params=params1)
            res = res.json()

            date = res["items"][0]["liveStreamingDetails"]["scheduledStartTime"]
            date = date.replace('T', ' ').replace('Z', '')
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            date = date + timedelta(hours=9)

            l = []
            l.append(author)
            l.append(channelId)
            l.append(title)
            l.append(video_id)
            l.append(thumbnail)
            l.append(date)
            lists.append(l)

        elif status == 'live':
            l = []
            l.append(author)
            l.append(channelId)
            l.append(title)
            l.append(video_id)
            l.append(thumbnail)
            l.append('配信中')
            lists.append(l)

        else:
            continue
        
        # lists = sorted(lists, key=lambda i: i[5])


    return render(request, 'mypage.html', {"lists": lists})