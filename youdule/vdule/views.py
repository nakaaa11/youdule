from datetime import timedelta
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
# from .subscription import get_subscriptions

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

def mypage(request):
    # channel_ids = get_subscriptions()
    channel_ids = ['UCRRKdB87Oj-FkqS4L9QQRiQ', 'UCjXBuHmWkieBApgBhDuJMMQ', 'UCoSrY_IQQVpmIRZ9Xf-y93g', 'UC8tryhd0liC1hIkYmir7k2w', 'UCkIimWZ9gBJRamKF0rmPU8w', 'UCutJqz56653xV2wwSvut_hQ', 'UC1opHUrw8rvnsadT-iGp7Cg', 'UCyLGcqYs7RsBb3L0SJfzGYA', 'UCuk7vapXKckSw6yCGGDspDg', 'UCCzUftO8KOVkV4wQG1vkUvg', 'UCln9P4Qm3-EAY4aiEPmRwEA', 'UC67Wr_9pA4I0glIxDt_Cpyw', 'UCzUNASdzI4PV5SlqtYwAkKQ', 'UCkkxn2ldlFUMupTlXU8meAw', 'UCPkKpOHxEDcwmUAnRpIu-Ng', 'UCiMG6VdScBabPhJ1ZtaVmbw', 'UCNTxclE0N4qsUuirssL_D8w', 'UCPKsFwt9ACF-EnJM3xN8wyQ', 'UCcxbWdwrs5B782K88ppAVMg', 'UCaak9sggUeIBPOd8iK_BXcQ', 'UCvUc0m317LWTTPZoBQV479A', 'UCENwRMx5Yh42zWpzURebzTw', 'UC7-N7MvN5muVIHqyQx9LFbA', 'UC10BM9XdLdrvB8japwmRUvA', 'UCnvVG9RbOW3J6Ifqo-zKLiw', 'UCFKOVgVbGmX65RxO3EtH3iw', 'UCdn5BQ06XqgXoAxIhbqw5Rg', 'UCIu-aUArYq_H84dBpCAokMA', 'UCihYMokYrglpPKgjzbZYgqA', 'UC1H5dv45x2aFKk-6JZLSWIQ', 'UCLLuaTElO1eRGOo2qc_Rdsw', 'UCPyNsNSTUtywkekbDdCA_8Q', 'UCIG9rDtgR45VCZmYnd-4DUw', 'UCMMBGMjrrWcRZmG_lW4jC-Q', 'UCJHZshDuIrd_6MaT8MIjFtg', 'UC9V3Y3_uzU5e-usObb6IE1w', 'UCljYHFazflmGaDr5Lo90KmA', 'UC5CwaMl1eIgY8h02uZw7u8A', 'UCuq1ynSBN4ROHC1bHJNlrWQ', 'UCeShTCVgZyq2lsBW9QwIJcw', 'UCo7TRj3cS-f_1D9ZDmuTsjw', 'UCXRlIK3Cw_TJIQC5kSJJQMg', 'UCt30jJgChL8qeT9VPadidSw', 'UCdyqAaZDKHXg4Ahi7VENThQ', 'UCchlf66z1NueAv8xY117Lmw', 'UCjT8HuAXPxiWV1R9nBeUbhw', 'UCp-5t9SrOQwXMU7iIjQfARg', 'UCIBY1ollUsauvVi4hW4cumw', 'UC5Kgc_HNzx4GJ-w4QMeeKiQ', 'UCqm3BQLlJfvkTsX_hvm0UmA', 'UCL_qhgtOy0dy1Agp8vkySQg', 'UCQY514VtpAastF9qI1mVr9w', 'UCfTnJmRQP79C4y_BMF_XrlA', 'UCMMjv61LfBy5J3AT8Ua0NGQ', 'UC5LyYg6cCA4yHEYvtUsir3g', 'UCD9Rctu_iqX1DP35iSm2e-Q', 'UC_6C9bvzBLtuUBr4Nf3OaGA', 'UCSLtABY4HHBqACq5Bl2yKXg', 'UCCRUu9e_C63-SLFqbNLwWEw', 'UCsuV4MRk_aB291SrchUVb4w', 'UCbqR8Pc4un1oKdgCIuiy1oQ', 'UCk5a240pQsTVT9CWPnTyIJw', 'UC7umTzIrIJq8Xh428lj0M5A', 'UC_4tXjqecqox5Uc05ncxpxg', 'UCim0N3tvLijU_I3jbJeJV8g', 'UCzlPvPryUKvWyAdmTmLoC7Q', 'UC_4eOFXyxfxh_hrvFD1fhzA', 'UCSpGd36AHfQSFrGeJ6G8esA', 'UCRQX-dpFt_osBpH71ItuuvA', 'UCbc8fwhdUNlqi-J99ISYu4A', 'UC1DCedRgGHBdm81E1llLhOQ', 'UC_vMYWcDjmfdpH6r4TTn1MQ', 'UCl8E6NsjN979gbMBdztF48g', 'UChAnqc_AY5_I3Px5dig3X1Q', 'UCdhLVXIImQM7z6f52fapubw', 'UC9hwDDT7femX1YJ_-HfSo7A', 'UCm0NgWsqFg66HlUXhfcfXfA', 'UC3UvC3byXL0o-daNS54m1Xg', 'UCmAutZSvFH5mkR9OoPtpOmQ', 'UCcd-GOvl9DdyPVHQxy58bOw', 'UCxNK9pearb-7ygj0OucNXYA', 'UC0xRMqPOyRNPTaL6BxhbCnQ', 'UCmLlUC6pE9zGhv06NZ20wxg', 'UCpGpA7mSYmNJjLiJxKso5QA', 'UCFXl12dZUPs7MLy_dMkMZYw', 'UCd6sVOxaZoX2NPrYw3nStdg', 'UCOk5YQTyq6B9lOZ1FqG54Jw', 'UCxbY38ReXW3LbaviWUE4omg', 'UC38hCsF3st1pBJBw8JnAu2g', 'UCQroUtPIMKyVFulhROUItog', 'UC_1GPhYlXI2ka2ji5gnqWFQ', 'UCL9jk-70ogMA_I2B79qZzQw', 'UCvpredjG93ifbCP1Y77JyFA', 'UCa0jR_r3D5f8MXeQZg6wMVw', 'UCM4FwhxLYLHlOSPnfxmxSQw', 'UCoKRTudLOqjgdIFpCZIkW4w', 'UCKSql-GFCO400w7xNFbYeug', 'UCHi5HD9w9B-gI6Lbx43Rs7A', 'UCU0JjQr0I0DIRwV8joRIIBA', 'UCKudwfXQgNM7Gkjv95qRI9w', 'UCPKbVouzvWhHeVvy0UbsRCQ', 'UCqI2gx2ep2mjzMXnbxeYiAQ', 'UCFo4kqllbcQ4nV83WCyraiw', 'UCg3qsVzHeUt5_cPpcRtoaJQ', 'UCzLVRcnb9W4Li-F3uH6ETRg', 'UCneJ64DqPjL7kWW5V0WUyhg', 'UCgeaC4OEk0t54m2hWQtjjIw', 'UCRIgIJQWuBJ0Cv_VlU3USNA', 'UC4lk0Ob-F3ptOQUUq8s0pzQ', 'UCDSs0Hc8W2klLs1Qs38tDDQ', 'UCDOTPjUW-NhQMDmYbgMvQKA', 'UCwA7Aepp7nRUJNa8roQ-6Bw', 'UC4X6IkoRWN_1YzXske2vOVg', 'UC2OgzdgLQ7vxlANVxF3kgvg', 'UC368TexZ5Rc3v5KuoDaJIfw', 'UCMsNS10PzxzEayT7UHS4p6g', 'UCVNANJylxTtNJ1fmeL04asw', 'UCdSu3tgroULNBpkyWkEzCYw', 'UCqAbcgEp4NqCRnLG3NVJezw', 'UChNxH3wxiElBSAdAyMfNhJQ', 'UCRp7ooQOmTpq52g0cfqLnhQ', 'UCOyXde8s_aKc5e0Ql2KCOYA', 'UCKHSCfxL1zWDfxeD60z6Hpg', 'UC_IFf-9qHWQmaAEkLjlD5eQ', 'UCSxwU949ET-h5aRYYKlVTfg', 'UC1wNLVbaYDUGFJ3sHGk2ozQ', 'UCcz9te8w1a1aHP8s2SPnXEA', 'UChv5yk_9B0YCWNRg9KvztyA', 'UCgBPuTX7crv_2jKAkH5z7bA', 'UCWdFb_w3JI1BPTiBCXERg2Q', 'UCIS8BB4C2cuzeILjQV9pxGA', 'UC40gs0opj389ohjLnJIAJzA', 'UCCv34n5TQavmOQqOOPEvFrA', 'UCSHzI-t58X8STwqjfSzp47w', 'UCljUAjufNh7VI0yElcAdlhg', 'UCosy7jwSdXUbLbJBYgyRcnw', 'UCNKcMBYP_-18FLgk4BYGtfw', 'UCwUmloRE3gmc4rkTRQI524Q', 'UC_Jzr6RtTKLyHJFUExLyPuQ', 'UCpOjLndjOqMoffA-fr8cbKA', 'UCPlreGCqby4Qg9Vuem5scpw', 'UCibEhpu5HP45-w7Bq1ZIulw', 'UCM6eCMr8omEsv9z92alIWEw', 'UCeqyNxU8ubbY4T7NTXo0BWg', 'UC3yoBf-u0Nt7nrxsq_j1vpQ', 'UC4C37AMho6DRUIYnoc4fiSA', 'UCcvLSRIWJIAGFDyWtzkbiHA', 'UCwAVKZKMkKNEMShMK68PuzA', 'UCwzROnLWBu6RYsRELYj7D5Q', 'UCG09qajPDZdPtLsTkW7mJQA', 'UCMGLrWp6VOuO9EkMEyfib9Q', 'UCJwGWV914kBlV4dKRn7AEFA', 'UCj29XmMyJJf7KyhuxST99eg']
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    videos_url = 'https://www.googleapis.com/youtube/v3/videos'

    titles = []
    thumbnails = []
    video_ids =[]
    dates = []
    # print(channel_ids) 
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
        print(r)
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

        dates.append(r["items"][0]["liveStreamingDetails"]["scheduledStartTime"])
        dates = dates + timedelta(hours=9)

    return render(request, 'mypage.html', {'dates':dates, 'titles':titles, 'thumbnails':thumbnails, 'video_ids':video_ids})