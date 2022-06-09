import json
from pprint import pprint
import feedparser
from bs4 import BeautifulSoup
import requests
import pandas as pd


mls_rdf = 'https://www.youtube.com/feeds/videos.xml?channel_id=UCRRKdB87Oj-FkqS4L9QQRiQ'
mls_dic = feedparser.parse(mls_rdf)
# print((mls_dic))
print(mls_dic['entries'][0]['links'])
print(mls_dic['entries'][0]['media_thumbnail'][0]['url'])
video_id = mls_dic['entries'][0]['yt_videoid']
title = mls_dic['entries'][0]['title']
thumbnail = mls_dic['entries'][0]['media_thumbnail'][0]['url']
author = mls_dic['entries'][0]['authors'][0]['name']
print(video_id, title, thumbnail, author)
# link = []
# videoId = []
# channelId = []
# title = []
# thumbnail = []
# author = []
# print(mls_dic)
# for entry in mls_dic.entries:
#     link.append(entry.link)
#     videoId.append(entry.yt_videoid)
#     channelId.append(entry.yt_channelid)
#     title.append(entry.title)
#     thumbnail.append(entry['media_thumbnail'][0]['url'])
#     author.append(entry['authors'][0]['name'])
#     print(link, videoId, channelId, title, thumbnail, author)
#     break


# print(mls_dic.entries['id'])

# #予定1
# /html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]/ytd-shelf-renderer/div[1]/div[1]/div/h2/div[1]/div/a/span

# #予定2
# /html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[1]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[3]/div[3]/ytd-shelf-renderer/div[1]/div[1]/div/h2/div[1]/div/a/span

# #予定3
# /html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]/ytd-shelf-renderer/div[1]/div[1]/div/h2/div[1]/div/a/span


