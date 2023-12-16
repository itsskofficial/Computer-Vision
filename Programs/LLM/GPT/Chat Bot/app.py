import os
import openai 
import argparse
from dotenv import *
from beautify import *

config = dotenv_values('../keys.env')

def main():

    parser = argparse.ArgumentParser(description = 'Command line chatbot with GPT')
    parser.add_argument('--personality', type = str, help = "A brief summary of the chatbot's personality", default = 'friendly and helpful')
    parser.add_argument('--envfile', type = str, default = '../keys.env', required = False, help = 'A dotenv file with your OPENAI_API_KEY')
    args = parser.parse_args()
    load_dotenv(args.envfile)

    if 'OPENAI_API_KEY' not in os.environ:
        raise ValueError('Missing OPENAI_API_KEY from environment. Please check your env file')
    
    openai.api_key = os.environ['OPENAI_API_KEY']

    bot_info = f'You are a conversational chatbot. Your personality is {args.personality}'
    greeting = red('Jarvis : ') + f'Hi there, I am Jarvis who is {args.personality}. How can I help you today?\n'
    messages = [
        {
            'role' : 'system',
            'content' : bot_info
        },
        {
            'role' : 'assistant',
            'content' : greeting
        }
    ]
    print(greeting)

    while True:
        try:
            user_input = input(blue('You : '))
            messages.append(
                {
                    'role' : 'user',
                    'content' : user_input
                }
            )
            response = openai.ChatCompletion.create(
                model = 'gpt-3.5-turbo',
                messages = messages
            )

            messages.append(response.to_dict()['choices'][0]['message'].to_dict())
            answer = response.to_dict()['choices'][0]['message'].to_dict()['content']
            print(f'{answer}\n')

        except KeyboardInterrupt:
            print('\n\nExiting...')
            exit(1)

if __name__ == '__main__':
    main()