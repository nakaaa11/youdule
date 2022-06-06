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
# from .subscription import get_subscriptions

CLIENT_SECRETS_FILE = '/Users/nak/Desktop/python_lesson/app/youdule/client_secrets.json'
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
    channelIds = ['UCRRKdB87Oj-FkqS4L9QQRiQ', 'UCjXBuHmWkieBApgBhDuJMMQ', 'UCoSrY_IQQVpmIRZ9Xf-y93g', 'UCkIimWZ9gBJRamKF0rmPU8w', 'UC8tryhd0liC1hIkYmir7k2w', 'UCutJqz56653xV2wwSvut_hQ', 'UC1opHUrw8rvnsadT-iGp7Cg', 'UCnvVG9RbOW3J6Ifqo-zKLiw', 'UCyLGcqYs7RsBb3L0SJfzGYA', 'UCuk7vapXKckSw6yCGGDspDg', 'UCln9P4Qm3-EAY4aiEPmRwEA', 'UCCzUftO8KOVkV4wQG1vkUvg', 'UC67Wr_9pA4I0glIxDt_Cpyw', 'UCiMG6VdScBabPhJ1ZtaVmbw', 'UCzUNASdzI4PV5SlqtYwAkKQ', 'UCkkxn2ldlFUMupTlXU8meAw', 'UCPkKpOHxEDcwmUAnRpIu-Ng', 'UCNTxclE0N4qsUuirssL_D8w', 'UCENwRMx5Yh42zWpzURebzTw', 'UCcxbWdwrs5B782K88ppAVMg', 'UCPKsFwt9ACF-EnJM3xN8wyQ', 'UCvUc0m317LWTTPZoBQV479A', 'UCaak9sggUeIBPOd8iK_BXcQ', 'UC7-N7MvN5muVIHqyQx9LFbA', 'UC10BM9XdLdrvB8japwmRUvA', 'UCFKOVgVbGmX65RxO3EtH3iw', 'UCdn5BQ06XqgXoAxIhbqw5Rg', 'UCIu-aUArYq_H84dBpCAokMA', 'UCihYMokYrglpPKgjzbZYgqA', 'UC1H5dv45x2aFKk-6JZLSWIQ', 'UCLLuaTElO1eRGOo2qc_Rdsw', 'UCPyNsNSTUtywkekbDdCA_8Q', 'UCIG9rDtgR45VCZmYnd-4DUw', 'UCMMBGMjrrWcRZmG_lW4jC-Q', 'UC9V3Y3_uzU5e-usObb6IE1w', 'UCljYHFazflmGaDr5Lo90KmA', 'UC5CwaMl1eIgY8h02uZw7u8A', 'UCuq1ynSBN4ROHC1bHJNlrWQ', 'UCeShTCVgZyq2lsBW9QwIJcw', 'UCo7TRj3cS-f_1D9ZDmuTsjw', 'UCdyqAaZDKHXg4Ahi7VENThQ', 'UCchlf66z1NueAv8xY117Lmw', 'UCXRlIK3Cw_TJIQC5kSJJQMg', 'UCjT8HuAXPxiWV1R9nBeUbhw', 'UCp-5t9SrOQwXMU7iIjQfARg', 'UCIBY1ollUsauvVi4hW4cumw', 'UC5Kgc_HNzx4GJ-w4QMeeKiQ', 'UCqm3BQLlJfvkTsX_hvm0UmA', 'UCL_qhgtOy0dy1Agp8vkySQg', 'UCfTnJmRQP79C4y_BMF_XrlA', 'UCMMjv61LfBy5J3AT8Ua0NGQ', 'UC5LyYg6cCA4yHEYvtUsir3g', 'UCD9Rctu_iqX1DP35iSm2e-Q', 'UC_6C9bvzBLtuUBr4Nf3OaGA', 'UCSLtABY4HHBqACq5Bl2yKXg', 'UCCRUu9e_C63-SLFqbNLwWEw', 'UCsuV4MRk_aB291SrchUVb4w', 'UCbqR8Pc4un1oKdgCIuiy1oQ', 'UCk5a240pQsTVT9CWPnTyIJw', 'UC7umTzIrIJq8Xh428lj0M5A']
    titles = ['CRカップ本戦頑張るぞ!! #大妖怪WIN【Apex/エーペックス】', '【DBD】ぶいすぽ血みどろ鬼ごっこ【ぶいすぽ/八雲べに】', '【MINECRAFT】GORBIUS', '˗ˋˏマイクラˎˊ˗ 夏祭りじゃないけど・・・〇〇〇〇だーー!!!!（ 天宮こころ/にじさんじ ）Minecraft', '#3 MOTHER2 リレー形式でクリアするまでやりたい生配信', '【歌枠】おひるのおうた！！KARAOKE Singing♪【湊あくあ/ホロライブ】', '【DBD 】ぶいすぽおにごっこ【ぶいすぽ/兎咲ミミ】', '【CRカップ本番 】とにかく頑張る作戦 【 ぶいすぽ / 花芽すみれ】', '【VALORANT】朝からカロリー高め。【緋月ゆい/ネオポルテ】', '【歌枠】～朗報～声帯結節がなくなっていた【ホロライブ/宝鐘マリン】', '学長お金の雑談ライブ\u3000センスの良い営業マン&amp;やるといったらやる！すぐやる！笑【6月6日9時15分まで】', '【CRCUP】フォールガイズとゴルフの王者になりたい【ぶいすぽ/花芽なずな】', '【ニチアサ】NICHI☆ASA【小森めと / ブイアパ】', '100万人突破する', '【APEX】おはようかじゅなど【ぶいすぽっ！/ 藍沢エマ】', '【歌枠│singing】上手に歌えたらアーカイブ残す歌【ラプラス・ダークネス/ホロライブ】', '【 APEX 】 プラチナだるまAPEX一ノ瀬フルうるはパランク', '【 Apex Legends 】記憶から消えたPWとメアドってどこに売ってますか？→ぶいすぽメンバーとDBD【ぶいすぽっ！/橘ひなの】', '【晩酌ライブ】飛騨牛、生雲丹、生牡蠣でおつまみ作り♪', '【雀魂】ちょろっと練習の成果ださせてくれやｗ圧勝すっから！ｗ【歌衣メイカ】', '【高音質・広告なし】心音・寝息・囁き バイノーラル雑談（Heartbeat, sleeping breath, whispers）※6日23時にアーカイブメン限【雪花ラミィ/ホロライブ】', '【ネタバレあり】 ララ狐は竜騎士となりエオルゼアを救う\u3000次元の狭間オメガ【ホロライブ/白上フブキ】', '【雀魂】魂天への道  調整ラウンド朝活編【遅延あり】', '【#雀魂】声優さんからVtuberまで！#たかちさひそすい麻雀 【多井隆晴/紗彩木ひそり/河崎翆/木村千咲】', '【PUBG】Vの者と配信者でPUBG！渋谷ハルさん、アベレージさん、ぺんぺんさん', '【完走】夏だ！宿題だ！24時間小1〜小6の夏休み宿題マラソンでみんなで宿題終わらせっぞ！！！', '【CRcup:にじAPEX】色々おつかれさまでした。【ラトナ・プティ/にじさんじ】', '新曲「転生林檎」を投稿しました。\u3000ゲスト：えいりな刃物さん', '【APEX】初めてヴァル使っちゃうよん！#にじさんじカスタム【星川サラ/にじさんじ】', '【ショート歌枠】歌＋告知＋お知らせの三本です【ホロライブ / 星街すいせい 】', '【麻雀コラボ】#郡東つねる【#雀魂 /天開司/因幡はねる/伊東ライフ/にじさんじ郡道美玲】', '【歌枠】ミニ告知あり！今日も歌うYO！Singing Stream【にじさんじ/町田ちま】', '#10【ドラクエ8】脳筋女騎士、新たな冒険に出る！！【白銀ノエル/ホロライブ】※ネタバレあり', '【PowerWash Simulator】屋根の斜度がすごい建物はやばい\u3000＃１０【戌亥とこ/にじさんじ】', '【クレーマー紹介スレ】欲望が人生を豊かにする【雑談】', '【 #朝ミオ 】６月だ！月曜日だ！朝みおーんだ！！！！', '【Portal2】お昼から穴に出したり入れたり超健全です！【沙花叉クロヱ/ホロライブ】', '【登録者２万人記念ライブ】Python学習のロードマップを公開！〜 初心者が勉強を進める順番やトピックを紹介 〜', '【誕生日カウントダウン】６歳の誕生日をみんなと一緒に迎えたい！【角巻わため/ホロライブ４期生】', '【DEATH AND TAXES】Only Two Things Are Certain in Life, yeah?', '【LIVE】ローランド＆「コミュ力」強化支援スペシャリストが「世界最高の話し方」を伝授【22:00〜23:00】', '【エンジニアチャンネル】エンジニアになるためのステップも解説するよー【お悩み相談】', 'いろいろ', '【APEX大会】FFL GGC 一次予選 グループB 神視点配信【shomaru7/エーペックスレジェンズ】', 'えぺまつり外伝Sじょじょおじ視点\u3000【APEX】', '【会見直前特番】アンジャッシュ渡部建さん緊急会見  半年ぶりの公の場 会見の注目ポイントをおさらい｜よる7時〜の会見はアプリでご視聴いただけます（無料）', '【APEX】にじさんじAPEX大会！！魔界ノりりむ&amp;文野環\u3000#チーム10WIN 【椎名唯華/にじさんじ】', '10万人をちょっと雑めに祝う配信', '【わらじお🍡】第8回おまつ×しくろのふたりわらじお', '【#にじさんじカスタム 】いよいよ本番\u3000暴れろ！【#HacKING_FUN】', '【ヴァルコネ】ぺこーらとラプちゃんがゲームに登場！絶対ゲットぺこ！【ホロライブ/兎田ぺこら】', '【重大告知あり】久々のセリフ枠！配信最後に重大告知あり🔥【風真いろは/ホロライブ6期生】', '年越しライブ！受験生応援！ドラゴンタケシ＆法律厳守ボンバーマンで1位を目指す！', 'えぺまつりにいざ参る【APEX LEGENDS】', '【アーカイブ】いまにゅがみなさんの質問・相談受け付けます', '誕生日だし、そろそろ正面向くか……#ういの誕生日会', 'しもふりチューブ久しぶりの生配信', '米雇用統計ショック、株価下落\u3000金利急上昇【LIVE】', '[LIVEアーカイブ] ジェレミー・ウェイド来日！LIVE Q&amp;A with Jeremy Wade | あなたの質問答えます！', '決着をつけよう・・・スパイギアさん【supported by GeForce NOW Powered by au】'] 
    thumbnails = ['https://i.ytimg.com/vi/L_W1DqUFeoM/default.jpg', 'https://i.ytimg.com/vi/-Dchv_vnqNQ/default.jpg', 'https://i.ytimg.com/vi/5QPIaKu7hjo/default.jpg', 'https://i.ytimg.com/vi/_jQeo9uWAw4/default.jpg', 'https://i.ytimg.com/vi/GKdNdDqAqOE/default.jpg', 'https://i.ytimg.com/vi/b59kreP24ac/default.jpg', 'https://i.ytimg.com/vi/tcyf7sRzxqo/default.jpg', 'https://i.ytimg.com/vi/ftDfk2CYCKY/default.jpg', 'https://i.ytimg.com/vi/waidXhXzID4/default.jpg', 'https://i.ytimg.com/vi/9mEJh8DBgTE/default.jpg', 'https://i.ytimg.com/vi/yYQnsxMu_l0/default.jpg', 'https://i.ytimg.com/vi/Ul8t-rE853E/default.jpg', 'https://i.ytimg.com/vi/70O68IltgjI/default.jpg', 'https://i.ytimg.com/vi/fxRLe1P8d7Q/default.jpg', 'https://i.ytimg.com/vi/_YQjZ2tt3Sk/default.jpg', 'https://i.ytimg.com/vi/aP0JTin7jgQ/default.jpg', 'https://i.ytimg.com/vi/moeozrK2cBY/default.jpg', 'https://i.ytimg.com/vi/sBOwnabUl04/default.jpg', 'https://i.ytimg.com/vi/sXXcbZWtpaQ/default.jpg', 'https://i.ytimg.com/vi/OirKe2iXmyM/default.jpg', 'https://i.ytimg.com/vi/IMdZbRRIRiM/default.jpg', 'https://i.ytimg.com/vi/skvpukmLPZw/default.jpg', 'https://i.ytimg.com/vi/blpF-Wm9T5w/default.jpg', 'https://i.ytimg.com/vi/EM5001ZXGYQ/default.jpg', 'https://i.ytimg.com/vi/mLxXZMCkpwo/default.jpg', 'https://i.ytimg.com/vi/ieE7U0UldhQ/default.jpg', 'https://i.ytimg.com/vi/q2nXQK8Mek8/default.jpg', 'https://i.ytimg.com/vi/vhS8YKPfFqg/default.jpg', 'https://i.ytimg.com/vi/qBsWu6YzHBQ/default.jpg', 'https://i.ytimg.com/vi/njGJGwx_eVM/default.jpg', 'https://i.ytimg.com/vi/Onn_yLmemrk/default.jpg', 'https://i.ytimg.com/vi/07ubGiObxpE/default.jpg', 'https://i.ytimg.com/vi/MwJQQiJaEkA/default.jpg', 'https://i.ytimg.com/vi/fQi3B1p1QHE/default.jpg', 'https://i.ytimg.com/vi/97tplb6T-QU/default.jpg', 'https://i.ytimg.com/vi/oSfqpkfcxNw/default.jpg', 'https://i.ytimg.com/vi/6J58iFMlcLQ/default.jpg', 'https://i.ytimg.com/vi/nRDQRaea6Aw/default.jpg', 'https://i.ytimg.com/vi/wUyUMQHsiZQ/default.jpg', 'https://i.ytimg.com/vi/14j8NnpaBtA/default.jpg', 'https://i.ytimg.com/vi/2u4uwRIt9yo/default.jpg', 'https://i.ytimg.com/vi/KVYQuSUoNe4/default.jpg', 'https://i.ytimg.com/vi/-vVgsR02WfU/default.jpg', 'https://i.ytimg.com/vi/p0qQZe6dBcg/default.jpg', 'https://i.ytimg.com/vi/xh6kXck5xzE/default.jpg', 'https://i.ytimg.com/vi/yMGb6dT2gJ0/default.jpg', 'https://i.ytimg.com/vi/p5UCxVcmUoA/default.jpg', 'https://i.ytimg.com/vi/pKgDJxAJV_A/default.jpg', 'https://i.ytimg.com/vi/djlL1ACMgag/default.jpg', 'https://i.ytimg.com/vi/hrJhxtFHyT4/default.jpg', 'https://i.ytimg.com/vi/SMwIgQCE4zs/default.jpg', 'https://i.ytimg.com/vi/tlPUkUGLA5w/default.jpg', 'https://i.ytimg.com/vi/3gMu4NY-vr4/default.jpg', 'https://i.ytimg.com/vi/oN4bkTTdLXc/default.jpg', 'https://i.ytimg.com/vi/N32B4E8cWBQ/default.jpg', 'https://i.ytimg.com/vi/KXu3LHa9QVs/default.jpg', 'https://i.ytimg.com/vi/aoNPzTbMP6k/default.jpg', 'https://i.ytimg.com/vi/9VtiHgJ1J-Y/default.jpg', 'https://i.ytimg.com/vi/6Nij87zSaYY/default.jpg', 'https://i.ytimg.com/vi/xnf_2LbanYE/default.jpg']
    videoIds =  ['L_W1DqUFeoM', '-Dchv_vnqNQ', '5QPIaKu7hjo', '_jQeo9uWAw4', 'GKdNdDqAqOE', 'b59kreP24ac', 'tcyf7sRzxqo', 'ftDfk2CYCKY', 'waidXhXzID4', '9mEJh8DBgTE', 'yYQnsxMu_l0', 'Ul8t-rE853E', '70O68IltgjI', 'fxRLe1P8d7Q', '_YQjZ2tt3Sk', 'aP0JTin7jgQ', 'moeozrK2cBY', 'sBOwnabUl04', 'sXXcbZWtpaQ', 'OirKe2iXmyM', 'IMdZbRRIRiM', 'skvpukmLPZw', 'blpF-Wm9T5w', 'EM5001ZXGYQ', 'mLxXZMCkpwo', 'ieE7U0UldhQ', 'q2nXQK8Mek8', 'vhS8YKPfFqg', 'qBsWu6YzHBQ', 'njGJGwx_eVM', 'Onn_yLmemrk', '07ubGiObxpE', 'MwJQQiJaEkA', 'fQi3B1p1QHE', '97tplb6T-QU', 'oSfqpkfcxNw', '6J58iFMlcLQ', 'nRDQRaea6Aw', 'wUyUMQHsiZQ', '14j8NnpaBtA', '2u4uwRIt9yo', 'KVYQuSUoNe4', '-vVgsR02WfU', 'p0qQZe6dBcg', 'xh6kXck5xzE', 'yMGb6dT2gJ0', 'p5UCxVcmUoA', 'pKgDJxAJV_A', 'djlL1ACMgag', 'hrJhxtFHyT4', 'SMwIgQCE4zs', 'tlPUkUGLA5w', '3gMu4NY-vr4', 'oN4bkTTdLXc', 'N32B4E8cWBQ', 'KXu3LHa9QVs', 'aoNPzTbMP6k', '9VtiHgJ1J-Y', '6Nij87zSaYY', 'xnf_2LbanYE']

    lists = []

    for i in range(len(channelIds)):
        l = []
        l.append(titles[i])
        l.append(videoIds[i])
        l.append(thumbnails[i])
        l.append(channelIds[i])
        lists.append(l)

    return render(request, 'need.html', {"lists": lists})


def mypage(request):
    print("start!!!")
    # channel_ids = get_subscriptions()
    channel_ids = ['UCRRKdB87Oj-FkqS4L9QQRiQ', 'UCjXBuHmWkieBApgBhDuJMMQ', 'UCoSrY_IQQVpmIRZ9Xf-y93g', 'UCkIimWZ9gBJRamKF0rmPU8w', 'UC8tryhd0liC1hIkYmir7k2w', 'UCutJqz56653xV2wwSvut_hQ', 'UC1opHUrw8rvnsadT-iGp7Cg', 'UCnvVG9RbOW3J6Ifqo-zKLiw', 'UCyLGcqYs7RsBb3L0SJfzGYA', 'UCuk7vapXKckSw6yCGGDspDg', 'UCln9P4Qm3-EAY4aiEPmRwEA', 'UCCzUftO8KOVkV4wQG1vkUvg', 'UC67Wr_9pA4I0glIxDt_Cpyw', 'UCiMG6VdScBabPhJ1ZtaVmbw', 'UCzUNASdzI4PV5SlqtYwAkKQ', 'UCkkxn2ldlFUMupTlXU8meAw', 'UCPkKpOHxEDcwmUAnRpIu-Ng', 'UCNTxclE0N4qsUuirssL_D8w', 'UCENwRMx5Yh42zWpzURebzTw', 'UCcxbWdwrs5B782K88ppAVMg', 'UCPKsFwt9ACF-EnJM3xN8wyQ', 'UCvUc0m317LWTTPZoBQV479A', 'UCaak9sggUeIBPOd8iK_BXcQ', 'UC7-N7MvN5muVIHqyQx9LFbA', 'UC10BM9XdLdrvB8japwmRUvA', 'UCFKOVgVbGmX65RxO3EtH3iw', 'UCdn5BQ06XqgXoAxIhbqw5Rg', 'UCIu-aUArYq_H84dBpCAokMA', 'UCihYMokYrglpPKgjzbZYgqA', 'UC1H5dv45x2aFKk-6JZLSWIQ', 'UCLLuaTElO1eRGOo2qc_Rdsw', 'UCPyNsNSTUtywkekbDdCA_8Q', 'UCIG9rDtgR45VCZmYnd-4DUw', 'UCMMBGMjrrWcRZmG_lW4jC-Q', 'UC9V3Y3_uzU5e-usObb6IE1w', 'UCljYHFazflmGaDr5Lo90KmA', 'UC5CwaMl1eIgY8h02uZw7u8A', 'UCuq1ynSBN4ROHC1bHJNlrWQ', 'UCeShTCVgZyq2lsBW9QwIJcw', 'UCo7TRj3cS-f_1D9ZDmuTsjw', 'UCdyqAaZDKHXg4Ahi7VENThQ', 'UCchlf66z1NueAv8xY117Lmw', 'UCXRlIK3Cw_TJIQC5kSJJQMg', 'UCjT8HuAXPxiWV1R9nBeUbhw', 'UCp-5t9SrOQwXMU7iIjQfARg', 'UCIBY1ollUsauvVi4hW4cumw', 'UC5Kgc_HNzx4GJ-w4QMeeKiQ', 'UCqm3BQLlJfvkTsX_hvm0UmA', 'UCL_qhgtOy0dy1Agp8vkySQg', 'UCfTnJmRQP79C4y_BMF_XrlA', 'UCMMjv61LfBy5J3AT8Ua0NGQ', 'UC5LyYg6cCA4yHEYvtUsir3g', 'UCD9Rctu_iqX1DP35iSm2e-Q', 'UC_6C9bvzBLtuUBr4Nf3OaGA', 'UCSLtABY4HHBqACq5Bl2yKXg', 'UCCRUu9e_C63-SLFqbNLwWEw', 'UCsuV4MRk_aB291SrchUVb4w', 'UCbqR8Pc4un1oKdgCIuiy1oQ', 'UCk5a240pQsTVT9CWPnTyIJw', 'UC7umTzIrIJq8Xh428lj0M5A', 'UC_4tXjqecqox5Uc05ncxpxg', 'UCim0N3tvLijU_I3jbJeJV8g', 'UCzlPvPryUKvWyAdmTmLoC7Q', 'UCSpGd36AHfQSFrGeJ6G8esA', 'UCRQX-dpFt_osBpH71ItuuvA', 'UCbc8fwhdUNlqi-J99ISYu4A', 'UC1DCedRgGHBdm81E1llLhOQ', 'UC_vMYWcDjmfdpH6r4TTn1MQ', 'UCl8E6NsjN979gbMBdztF48g', 'UCm0NgWsqFg66HlUXhfcfXfA', 'UC3UvC3byXL0o-daNS54m1Xg', 'UCmAutZSvFH5mkR9OoPtpOmQ', 'UCxNK9pearb-7ygj0OucNXYA', 'UC0xRMqPOyRNPTaL6BxhbCnQ', 'UCt30jJgChL8qeT9VPadidSw', 'UCmLlUC6pE9zGhv06NZ20wxg', 'UCpGpA7mSYmNJjLiJxKso5QA', 'UCFXl12dZUPs7MLy_dMkMZYw', 'UCd6sVOxaZoX2NPrYw3nStdg', 'UCOk5YQTyq6B9lOZ1FqG54Jw', 'UCxbY38ReXW3LbaviWUE4omg', 'UC38hCsF3st1pBJBw8JnAu2g', 'UCL9jk-70ogMA_I2B79qZzQw', 'UCvpredjG93ifbCP1Y77JyFA', 'UCJHZshDuIrd_6MaT8MIjFtg', 'UCa0jR_r3D5f8MXeQZg6wMVw', 'UCM4FwhxLYLHlOSPnfxmxSQw', 'UCoKRTudLOqjgdIFpCZIkW4w', 'UCKSql-GFCO400w7xNFbYeug', 'UCHi5HD9w9B-gI6Lbx43Rs7A', 'UCKudwfXQgNM7Gkjv95qRI9w', 'UCPKbVouzvWhHeVvy0UbsRCQ', 'UCqI2gx2ep2mjzMXnbxeYiAQ', 'UCFo4kqllbcQ4nV83WCyraiw', 'UCg3qsVzHeUt5_cPpcRtoaJQ', 'UCzLVRcnb9W4Li-F3uH6ETRg', 'UCneJ64DqPjL7kWW5V0WUyhg', 'UCgeaC4OEk0t54m2hWQtjjIw', 'UCRIgIJQWuBJ0Cv_VlU3USNA', 'UCDSs0Hc8W2klLs1Qs38tDDQ', 'UCwA7Aepp7nRUJNa8roQ-6Bw', 'UCMsNS10PzxzEayT7UHS4p6g', 'UCqAbcgEp4NqCRnLG3NVJezw', 'UC_IFf-9qHWQmaAEkLjlD5eQ', 'UCSxwU949ET-h5aRYYKlVTfg', 'UC1wNLVbaYDUGFJ3sHGk2ozQ', 'UCgBPuTX7crv_2jKAkH5z7bA', 'UCWdFb_w3JI1BPTiBCXERg2Q', 'UCwUmloRE3gmc4rkTRQI524Q', 'UCM6eCMr8omEsv9z92alIWEw', 'UC3yoBf-u0Nt7nrxsq_j1vpQ', 'UCcvLSRIWJIAGFDyWtzkbiHA', 'UCG09qajPDZdPtLsTkW7mJQA']
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

        # if r["error"]["code"] == 403:
        #     print('The request cannot be completed because you have exceeded your <a href="/youtube/v3/getting-started#quota">quota</a>.')

        try:
            titles.append(r["items"][0]["snippet"]["title"])
            thumbnails.append(r["items"][0]["snippet"]["thumbnails"]["default"]["url"])
            video_ids.append(r["items"][0]["id"]["videoId"])

        except:
            pass

    print(titles, thumbnails, video_ids)
            
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
            # dates = dates + timedelta(hours=9)

        except:
            pass

    print(dates)
    lists = []
    try:
        for i in range(len(dates)):
            l = []
            l.append(dates[i])
            l.append(titles[i])
            l.append(thumbnails[i])
            l.append(video_ids[i])
            lists.append(l)
    except:
        pass
    print(lists)
    return render(request, 'mypage.html', {"lists": lists})