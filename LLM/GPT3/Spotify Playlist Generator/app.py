import os
import openai
import spotipy
import argparse
from dotenv import *

parser = argparse.ArgumentParser(description = 'An AI assistant which generates a Spotify playlist from user input text')
parser.add_argument('--envfile', help = 'A file which contains your OPENAI_API_KEY', default = '../keys.env', type = str)
args = parser.parse_args()
load_dotenv('../keys.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

sp = spotipy.Spotify(
    auth_manager = spotipy.SpotifyOAuth(
        client_id = os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri = 'http:/localhost:9999',
        scope = 'playlist-modiy-private'

    )
)

spotify_user = sp.current_user
assert spotify_user is not None

spotify_search_results = sp.search(
    q = item[0]['song'],
    type = 'track',
    limit = 3
)

track_id = spotify_search_results['tracks']['items'][0]['id']

sp.user_playlist_create(
    spotify_user,
    public = False,
    name = prompt
)

sp.user_playlist_add_tracks(
    current_user['id']
)

BOT_INFO = """
You are a helpful playlist generating assistant. You should generate a list of songs and their artist according to a text prompt.
Desired format : <serial_no>. <song_name> by <artist_name>
Don't include any introductory or ending lines
"""

def get_json_array_from_list(text):
    json_array = []
    text = text.split('\n')
    for item in text:
        song = item.split('.')[1].strip().split('by')[0].strip()
        artist = item.split('.')[1].strip().split('by')[1].strip()
        json_array.append(
            {
                'song' : song,
                'artist' : artist
            }
        )
    return json_array

def get_songs_from_prompt(prompt, count = 10):

    messages = [
        {
            'role' : 'system',
            'content' : BOT_INFO
        },
        {
            'role' : 'user',
            'content' : f'Generate a playlist of {count} songs based on the prompt {prompt}'
        }
    ]

    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages
    )

    answer = response.to_dict()['choices'][0]['message'].to_dict()['content']
    print(answer)
    json_array = get_json_array_from_list(answer)
    print(json_array)
