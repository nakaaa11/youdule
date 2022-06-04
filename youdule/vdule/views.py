from urllib import response
import requests
from django.shortcuts import redirect, render
import json
from django.conf import settings
from vdule.forms import UserForm
from .models import schedules, streamer
from .forms import Form
from .search_channel_id import search_channel_ids
from django.contrib.auth.decorators import login_required
import google_auth_oauthlib.flow
import google.oauth2.credentials

CLIENT_SECRETS_FILE = 'client_secret.json'
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

        if r["pageInfo"]["totalResults"] == 0:
            return render(request, 'index.html')

        else:
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

@login_required
def need(request):
    return render(request, 'need.html')

# def logged_out(request):
#     return render(request, 'registration/logged_out.html')


# def auth():
#   # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
#     flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#         CLIENT_SECRETS_FILE, scopes=SCOPES)

#   # The URI created here must exactly match one of the authorized redirect URIs
#   # for the OAuth 2.0 client, which you configured in the API Console. If this
#   # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
#   # error.
#     flow.redirect_uri = 'http://127.0.0.1:8000'

#     authorization_url = flow.authorization_url(
#          # Enable offline access so that you can refresh an access token without
#          # re-prompting the user for permission. Recommended for web server apps.
#         access_type= 'offline',
#           prompt = 'consent',
#         include_granted_scopes = 'true')
#           # Enable incremental authorization. Recommended as a best practice.

#   # Store the state so the callback can verify the auth server response.


#     return redirect(authorization_url)