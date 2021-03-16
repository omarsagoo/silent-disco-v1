import requests

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
# BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
# track_id = '6y0igZArWVi6Iz0rj35c1Y'


BASE_URL = 'https://api.spotify.com/v1/'
r = requests.get(BASE_URL + 'search?q=SickoMode&type=track&market=US', headers=headers)
# r = r.json()
# print(r.text)

import json
parsed = json.loads(r.text)
r = (json.dumps(parsed, indent=4, sort_keys=True))

for album in r['items']:
    print(album['name'], ' --- ', album['release_date'])


# actual GET request with proper header
# r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

# r = r.json()
# print(r)

# BASE_URL = 'https://api.spotify.com/v1/'
# r = requests.get(BASE_URL + 'search?q=tania%20bowra&type=artist', headers=headers)
# r = r.json()