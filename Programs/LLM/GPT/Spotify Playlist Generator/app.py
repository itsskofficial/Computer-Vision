import os
import openai
import spotipy
import argparse
from dotenv import *
from helpers import *

def main():
    parser = argparse.ArgumentParser(description = 'An AI assistant which generates a Spotify playlist from user input text')
    parser.add_argument('--envfile', help = 'A file which contains your OPENAI_API_KEY', default = '../keys.env', type = str, required = False)
    args = parser.parse_args()
    load_dotenv(args.envfile)
    openai.api_key = os.getenv('OPENAI_API_KEY')

    sp = spotipy.Spotify(
        auth_manager = spotipy.SpotifyOAuth(
            client_id = os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri = 'http://localhost:9999',
            scope = 'playlist-modify-private'
        )
    )

    spotify_user = sp.current_user()
    
    assert spotify_user is not None
    
    print('Hi there, I will generate a Spotify playlist for you based on any mood\n')
    prompt = input('Enter the description of the playlist mood you wanna create : ')
    count = int(input('Enter the number of songs you wanna add in your playlist : '))
    print('\nGreat! Here are the song I found for you\n')

    songs = get_songs_from_prompt(prompt, count)

    print('\nCreating a Spotify playlist for you...')

    spotify_playlist = sp.user_playlist_create(
        spotify_user['id'],
        public = False,
        name = prompt
    )
    create_spotify_playlist(sp, spotify_user, spotify_playlist, songs)
    
    print(f"\nYour playlist is created\nCheck it out at https://open.spotify.com/playlist/{spotify_playlist['id']}")

if __name__ == '__main__':
    main()