import openai
from data import *

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

def get_songs_from_prompt(prompt = 'happy songs', count = 10):

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
    songs = get_json_array_from_list(answer)
    return songs

def create_spotify_playlist(sp, spotify_user, spotify_playlist, songs):
    spotify_tracks = []
    for song in songs:
        song_name = song['song']
        artist_name = song['artist']
        spotify_search_results = sp.search(
            q = f'{song_name} {artist_name}',
            type = 'track',
            limit = 3
        )

        spotify_track = spotify_search_results['tracks']['items'][0]['id']
        spotify_tracks.append(spotify_track)
    
    sp.user_playlist_add_tracks(
        spotify_user['id'],
        spotify_playlist['id'],
        spotify_tracks
    )