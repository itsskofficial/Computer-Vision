import os
import openai
import argparse
from dotenv import *

parser = argparse.ArgumentParser(description = 'An AI assistant which generates a Spotify playlist from user input text')
parser.add_argument('--envfile', help = 'A file which contains your OPENAI_API_KEY', required = False, default = '../keys.env', type = str)
args = parser.parse_args()
load_dotenv(args.envfile)
openai.api_key = os.environ['OPENAI_API_KEY']

BOT_INFO = """
You are a helpful playlist generating assistant. You should generate a list of songs and their artist according to a text prompt.
"""

def get_json_from_list(text):
    dictionary = []
    text = text.split('\n')
    for item in text:
        song = item.split('.')[1].

        
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