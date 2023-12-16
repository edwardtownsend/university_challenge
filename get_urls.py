import os
import json
from googleapiclient.discovery import build

API_KEY = 'AIzaSyDJYqUjnTIwIQDJHQbLn4fCVug7eqgItds'  
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

playlist_ids = {42: 'PL507A34B0A4A00780', 43: 'PLAX-_7Q7UeorUGH05LshLhNfQvYzvAz7T', 44: 'PLKP-A43MqtTiRHZVEXvb2AyzMoSavfCXn', 45: 'PLKP-A43MqtTh2nEKxz4_43_gr8renD-c6', 46: 'PLrlSc8gCDlys4nS_WMnxzHKgIzPXXtn7Z', 47: 'PLxmwGyQNoPELQh6eQoW9yJNbr5YP-IoMr', 48: 'PLxmwGyQNoPEKYg_kCHAguScKgNxc7kvhN', 49: 'PLhpnwoA0FCobq3wnjD_fenXDl6LR2DR1v', 51: 'PLhpnwoA0FCobVbppZJJEyI1xlRDXqQT_S', 52: 'PLhpnwoA0FCoYhtuLY_yxyijZb7G52EyBb'}

def get_playlist_items(api_key, playlist_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=api_key)

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

def playlist_to_urls(api_key, playlist_id):
    playlist_items = get_playlist_items(api_key, playlist_id)

    video_urls = []
    for item in playlist_items:
        video_id = item['contentDetails']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video_urls.append(video_url)

    return video_urls


if __name__ == '__main__':
    output_file = 'video_urls.json'
    video_urls = {}
    for key, value in playlist_ids.items():
        playlist_id = value
        video_urls[key] = playlist_to_urls(API_KEY, playlist_id)

    with open(output_file, 'w') as file:
        json.dump(video_urls, file, indent=2)

    print(f"Video URLs written to {output_file}.")