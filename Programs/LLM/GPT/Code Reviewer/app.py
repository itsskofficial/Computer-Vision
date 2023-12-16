import os
import openai
import argparse
from dotenv import *


BOT_INFO = """
You will receive a file's contents as text
You will generate a code review for the file. Indicate what changes should be made to improve
its style, performance, readability, and maintainability. If there are any reputable libraries that could be introduced to improve the code, suggest them. Be kind and constructive. For each suggested change, include the line numbers to which you are referring
"""

def make_code_review(file_contents, model):
    messages = [
        {
            'role' : 'system',
            'content' : BOT_INFO
        },
        {
            'role' : 'user',
            'content' : f'Code review the following file : {file_contents}'
        }
    ]

    response = openai.ChatCompletion.create(
        model = model,
        messages = messages
    )

    answer = response.to_dict()['choices'][0]['message'].to_dict()['content']
    print(answer)

def init_code_review(file_path, model):
    with open(file_path, 'r') as file:
        contents = file.read()
    make_code_review(contents, model)


def main() : 
    parser = argparse.ArgumentParser(description = 'A simple code reviewer made with GPT')
    parser.add_argument('--file', help = 'File you want to review', type = str, default = 'test.py', required = True)
    parser.add_argument('--model', help = 'Model with which you want to review', type = str, default = 'gpt-3.5-turbo')
    args = parser.parse_args()
    init_code_review(args.file, args.model)

if __name__ == '__main__' :
    load_dotenv('../keys.env')
    openai.api_key = os.getenv('OPENAI_API_KEY')
    main()

