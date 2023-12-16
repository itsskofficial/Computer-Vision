import openai
import json
from flask import Flask, render_template, request
from dotenv import *

config  = dotenv_values('../keys.env')
openai.api_key = config['OPENAI_API_KEY']

def get_colors(prompt):
    text = f'''
    You are a color palette generating assistant that responds to text prompts
    for color palettes. You should generate color palettes that fit the theme,
    mood or instructions in the prompt. The nuumber of colors can be upto 5 colors

    Example 1
    Q : Convert the following verbal description into a color pallete with atmost 5 colors: a spicy pizza
    A : ["#9c3434", "#ffd88c", "#a9740e", "#6b3b00", "#78685a"]

    Example 2
    Q : Convert the following verbal description into a color pallete with atmost 5 colors: a calm beach
    A : ["#aeffab", "#abffc6", "#abffdf", "#abecff", "#abd7ff"]

    Desired Format : a JSON array of hexadecimal color codes

    Q : Convert the following verbal description into a color pallete with atmost 5 colors: {prompt}
    A :
    '''
    response = openai.Completion.create(
        prompt = text,
        model = 'text-davinci-003',
        max_tokens = 100
    )

    colors = json.loads(response['choices'][0]['text'])
    return colors

app = Flask(__name__,
            template_folder = 'templates',
            static_url_path = '',
            static_folder = 'static')

@app.route('/palette', methods = ['POST'])
def prompt_to_palette():
    query = request.form.get('query')
    colors = get_colors(query)
    return {"colors" : colors}
    

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == 'main':
    app.run(debug = True)