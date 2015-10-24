from flask import Flask, request, json, jsonify
from knapsack import knapsack
import requests
from base64 import b64encode

SPOTIFY_CLIENT_ID = "29a0ec9178864f69b5e5e181811254ed"
SPOTIFY_CLIENT_SECRET = "fc6b7b56e4154359a1b8569aece1301b"

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

@app.route('/')
def hello_world():
    return 'This is a!'

@app.route('/tracks_for_duration')
def tracks_for_duration():
    playlist_id = request.args.get('playlist_id')
    duration = request.args.get('duration')

    url_base = "https://api.spotify.com/v1/users/%s/playlists/%s/tracks"

    tracks = call_spotify_api_get(url_base % ("spotify", playlist_id)).json()['items']
    lengths = [item['track']['duration_ms'] / 1000 for item in tracks]

    indices_to_play = knapsack(lengths, lengths, len(lengths), int(duration))
    tracks_to_play = [tracks[i] for i in indices_to_play]

    return jsonify(tracklist=tracks_to_play)


@app.route('/update_tracklist')
def update_tracklist():
    pass

@app.route('/just_play')
def just_play():
    pass



if __name__ == '__main__':
    app.run(debug=True)
