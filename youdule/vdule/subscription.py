def get_subscriptions():
  import os
  import sys

  import httplib2
  from googleapiclient.discovery import build
  from oauth2client.client import flow_from_clientsecrets
  from oauth2client.file import Storage
  from oauth2client.tools import argparser, run_flow

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
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)

  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

  # This code creates a new, private playlist in the authorized user's channel.
  r = youtube.channels().list(
    part="snippet",
    mine="True",
  ).execute()

  channel_id = r["items"][0]["id"]

  subscriptions_list = []

  request = youtube.subscriptions().list(
    part="snippet",
    channelId=channel_id,
    maxResults=50,
    fields="nextPageToken, items/snippet/resourceId/channelId"
  )

  while request:
    response = request.execute()
    subscriptions_list.extend(list(map(lambda item: item["snippet"]["resourceId"]["channelId"], response["items"])))
    request = youtube.subscriptions().list_next(request, response)

  # subscriptions = subscriptions_list[0]
  print(subscriptions_list)
  return subscriptions_list
