import os
import openai
import argparse
from dotenv import *

argparse = argparse.ArgumentParser(description = 'A ')
load_dotenv('../keys.env')

BOT_INFO = """
You are a helpful playlist generating assistant. You should generate a list of songs and their artist according to a text prompt
"""

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