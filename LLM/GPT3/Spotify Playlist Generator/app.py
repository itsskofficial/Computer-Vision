import os
import json
import openai
import argparse
from dotenv import *

parser = argparse.ArgumentParser(description = 'An AI assistant which generates a Spotify playlist from user input text')
parser.add_argument('--envfile', help = 'A file which contains your OPENAI_API_KEY', default = '../keys.env', type = str)
args = parser.parse_args()
load_dotenv('../keys.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

BOT_INFO = """
You are a helpful playlist generating assistant. You should generate a list of songs and their artist according to a text prompt.
Desired format : <serial_no>. <song_name> by <artist_name>
Don't include any introductory or ending lines
"""

def get_json_array_from_list(text):
    json_array = []
    text = text.split('\n')
    print(text)
    for item in text:
        song = item.split('.')[1].strip().split('by')[0].strip()
        print(song)
        artist = item.split('.')[1].strip().split('by')[1].strip()
        # #json_array.append(
        #     {
        #         'song' : song,
        #         'artist' : artist
        #     }
        # )
    #return json_array
        
messages = [
    {
        'role' : 'system',
        'content' : BOT_INFO
    },
    {
        'role' : 'user',
        'content' : 'Generate a playlist of 10 top egoistic songs'
    }
]

response = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = messages
)

answer = response.to_dict()['choices'][0]['message'].to_dict()['content']
print(answer)
#json_array = get_json_array_from_list(answer)
get_json_array_from_list(answer)
#print(json_array)
