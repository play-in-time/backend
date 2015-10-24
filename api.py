from flask import Flask, request, json, jsonify
from knapsack import knapsack
import requests
from base64 import b64encode

SPOTIFY_CLIENT_ID = "29a0ec9178864f69b5e5e181811254ed"
SPOTIFY_CLIENT_SECRET = "fc6b7b56e4154359a1b8569aece1301b"

PLAYLISTS = [
    {
        'playlist_name': "Feel Good Indie Rock",
        'playlist_id': "0XUlpafP8eIlIWt3VHSd7q",
        'user_id': "spotify",
    },
    {
        'playlist_name': "Have a Great Day!",
        'playlist_id': "2PXdUld4Ueio2pHcB6sM8j",
        'user_id': "spotify",
    },
    {
        'playlist_name': "Teen Pop!",
        'playlist_id': "445ES7sgFV8zJHebmbUW0L",
        'user_id': "spotify",
    },
    {
        'playlist_name': "Epic Party",
        'playlist_id': "5cdgwETxybr7tWcr7RTiCO",
        'user_id': "spotify",
    },
    {
        'playlist_name': "Afternoon Acoustic",
        'playlist_id': "16BpjqQV1Ey0HeDueNDSYz",
        'user_id': "spotify",
    },
    {
        'playlist_name': "Good Vibes",
        'playlist_id': "3xgbBiNc7mh3erYsCl8Fwg",
        'user_id': "spotify",
    },
]

app = Flask(__name__)


""" Authorizes session with Spotify

    returns: Spotify access token
"""
def authorize_spotify():
    url = "https://accounts.spotify.com/api/token"
    payload = {
        'grant_type': 'client_credentials',
    }
    client = b64encode(SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET)
    headers = {
        'Authorization': 'Basic %s' % client,
    }

    response = requests.post(url=url, data=payload, headers=headers)

    return response.json()['access_token']

def call_spotify_api_get(url, access_token=None):
    access_token = access_token or authorize_spotify()

    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    return requests.get(url=url, headers=headers)

def get_tracks(playlist_id, user_id="spotify"):
    url_base = "https://api.spotify.com/v1/users/%s/playlists/%s/tracks"

    response = call_spotify_api_get(url_base % (user_id, playlist_id))

    try:
        tracks = response.json()['items']
    except:
        raise Exception("Spotify error: %s" % response.status_code)
    
    return tracks

""" Run knapsack algorithm for list of tracks
    
    Parameters:
      tracks: total pool of tracks to choose songs from

    returns: serialized json of desired tracklist
"""
def knapsack_from_tracks(tracks, duration):
    lengths = [item['track']['duration_ms'] / 1000 for item in tracks]

    indices_to_play = knapsack(lengths, lengths, len(lengths), int(duration))
    tracks_to_play = [tracks[i] for i in indices_to_play]

    play_length = sum(lengths[i] for i in indices_to_play)
    print "target:   %s\nachieved: %s\n" % (duration, play_length)

    return jsonify(tracklist=tracks_to_play)
    
@app.route('/')
def hello_world():
    return 'This is a!'

@app.route('/tracks_for_duration')
def tracks_for_duration():
    playlist_id = request.args.get('playlist_id')
    duration = request.args.get('duration')

    tracks = get_tracks(playlist_id)

    return knapsack_from_tracks(tracks, duration)

@app.route('/update_tracklist', methods=['POST'])
def update_tracklist():
    post_info = request.get_json(force=True)

    playlist_id = post_info['id']
    time_left = post_info['duration']

    songs_played = post_info['played']

    tracks = get_tracks(playlist_id)

    tracks_not_used = [item for item in tracks if item not in songs_played]

    return knapsack_from_tracks(tracks_not_used, time_left)


@app.route('/just_play')
def just_play():
    duration = request.args.get('duration')

    tracks = []
    for playlist in PLAYLISTS:
        tracks.extend(get_tracks(playlist['playlist_id'], playlist['user_id']))
    return knapsack_from_tracks(tracks, duration)


if __name__ == '__main__':
    app.run(debug=True)

