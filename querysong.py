import requests
import spotipy
import urllib.parse
import urllib.request
import re
from pytube import YouTube
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '69c20fe2830f4f2eab286331ffe88702'
CLIENT_SECRET = 'ed3cec28b71a4b6e8cd7997c17ed87d3'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

#Need to pass access token into header to send properly formed GET request to API server
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


# base URL of all Spotify API endpoints
# Track ID from the URI
# track_id = '6y0igZArWVi6Iz0rj35c1Y'


BASE_URL = 'https://api.spotify.com/v1/'
r = requests.get(BASE_URL + 'search?q=SickoMode&type=track&market=US', headers=headers)
d = r.json()
print(r.text)

path = input("Enter the path of your file: ") #C:\Users\---\Desktop\
uri = input("Enter the Spotify playlist uri: ") #spotify:playlist:4FroAeQwZrJCYYyJroHd9V
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id='b714b08a81b3470ab939354358c324c8', client_secret='83a32642aa4646009294ac6430b65dbe'))

import json
parsed = json.loads(r.text)
(json.dumps(parsed, indent=4, sort_keys=True))

songs = spotify.playlist_items(uri)
tracks = []

for i, playlist in enumerate(songs['items']):
    # [[Songs0, Artist0], [Songs1, Artist1]]
    tracks.append([songs['items'][i]['track']['name'], songs['items'][i]['track']['artists'][0]['name']])

for song in tracks:
    songToSearch = ' '.join([song[0], song[1]])
    query = urllib.parse.quote(songToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    html = urllib.request.urlopen(url)
    video_links = re.findall(r'watch\?v=(\S{11})', html.read().decode())
    YouTube('https://www.youtube.com/watch?v=' + video_links[0]).streams.first().download(path)
    

# actual GET request with proper header
# r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

# r = r.json()
# print(r)

# BASE_URL = 'https://api.spotify.com/v1/'
# r = requests.get(BASE_URL + 'search?q=tania%20bowra&type=artist', headers=headers)
# r = r.json()