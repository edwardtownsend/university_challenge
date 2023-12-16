import os
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from httplib2 import Credentials

API_KEY = 'AIzaSyDJYqUjnTIwIQDJHQbLn4fCVug7eqgItds'
CLIENT_SECRETS_FILE = 'client_secret_205179523744-vdb3d0knl7snhi11jlhdlue75kcd29db.apps.googleusercontent.com.json'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_authenticated_service():
    credentials = None

    # The file path to your downloaded JSON file containing OAuth client credentials
    CLIENT_SECRETS_FILE = 'client_secret_205179523744-vdb3d0knl7snhi11jlhdlue75kcd29db.apps.googleusercontent.com.json'

    # Attempt to load existing credentials from the file
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json')

    # If no valid credentials are available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, ['https://www.googleapis.com/auth/youtube.force-ssl'])
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)


def get_video_transcript(youtube, video_id):
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    video_title = video_response['items'][0]['snippet']['title']

    transcript_request = youtube.captions().list(
        part='snippet',
        videoId=video_id
    )
    transcript_response = transcript_request.execute()

    if 'items' in transcript_response and transcript_response['items']:
        transcript_id = transcript_response['items'][0]['id']
        transcript_details = youtube.captions().download(
            id=transcript_id,
            tfmt='srt'
        ).execute()
        transcript_text = transcript_details.decode('utf-8')
        return video_title, transcript_text

    return video_title, None

def get_playlist_items(youtube, playlist_id):
    playlist_items = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        playlist_items.extend(playlist_response['items'])
        next_page_token = playlist_response.get('nextPageToken')

        if not next_page_token:
            break

    return playlist_items


def main():
    youtube = get_authenticated_service()
    playlist_id = 'PLhpnwoA0FCoYhtuLY_yxyijZb7G52EyBb'
    playlist_items = get_playlist_items(youtube, playlist_id)

    for item in playlist_items:
        video_id = item['contentDetails']['videoId']
        video_title, transcript = get_video_transcript(youtube, video_id)

        print(f"Video Title: {video_title}")
        print("Transcript:")
        print(transcript)
        print("=" * 50)

if __name__ == '__main__':
    main()
