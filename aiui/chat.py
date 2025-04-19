from flask import Flask, render_template, request, jsonify
import requests, json, markdown,time
from datetime import datetime
from dotenv import load_dotenv
from api import *
import os

# spinup flask
app = Flask(__name__)
# Create record of the conversation
now = datetime.now()
logfile = f'conversation_{now.month}-{now.day}-{now.year}-{now.hour}.md'

load_dotenv()
api_url = os.environ['URL']

model = "gemma3:4b"


# Function to call Ollama API (example function)
def call_ollama_api(text, api_url):
    global model
    # Set up the headers and data for the request
    headers = {'Content-Type': 'application/json',}
    data = {"model": model, "messages": [{"role": "user", "content": text}]}
    # make the request
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        result = ''
        for line in response.text.splitlines():
            result += json.loads(line)["message"]["content"]
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return "API Error"


def send_ollama_image(data,model):
    # Set up the headers and data for the request
    headers = {'Content-Type': 'application/json', }
    data = {"model": model,
      "prompt":"Please caption this image",
      "images":data}
    # make the request
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        result = ''
        for line in response.text.splitlines():
            result += json.loads(line)["message"]["content"]
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        return "API Error"


@app.route("/submit", methods=["POST"])
def submit():
    global model
    tstamp1 = time.ctime()
    user_message = request.form.get('user_input')
    client = setup_client(api_url)
    bot_response = ask_model(client,model,user_message)
    msg_md = markdown.markdown(bot_response['message']['content'])
    tstamp2 = time.ctime()
    reply_content = f' [{tstamp2}] **Response:**\n```html\n<html>{msg_md}\n</html>```'
    # append conversation data to logfile
    with open(logfile, 'a') as f:
        f.write(f'### [{tstamp1}] User:\n```{user_message}```\n###{reply_content}\n')
    return render_template('index.html', user_message=user_message, bot_response=msg_md)


@app.route("/image_upload", methods=["POST"])
def image_upload():
    user_message = request.form.get('file_upload')
    # figure out how to properly send and receive the images to ollama
    bot_response = send_ollama_image(user_message)
    msg_md = markdown.markdown(bot_response)
    return render_template('index.html', user_message=user_message, bot_response=msg_md)


@app.route('/', methods=['GET'])
def index():
    user_message = None
    bot_response = None
    return render_template('index.html', user_message=user_message, bot_response=bot_response)


@app.route('/models', methods=['GET'])
def display_models():
    client = setup_client(api_url)
    models = list_models(client)
    return render_template('models.html', models=models)


# TODO: make get-model method (download new models)
# TODO: make delete model method
# TODO: make switch model method (one being used for chat)
@app.route('/switch-model', methods=['GET'])
def change_model():
    client = setup_client(api_url)
    models = list_models(client)
    return render_template('switch_model.html', models=models)


@app.route('/change-model/<new_model>', methods=['GET'])
def toggle_model_name(new_model):
    global model
    model = new_model
    user_message = None
    bot_response = None
    return render_template('index.html', user_message=user_message, bot_response=bot_response)


# TODO: Fix Image Upload functionality


if __name__ == '__main__':
    # create logfile
    with open(logfile, 'w') as f:
        f.write(f'# Log Created\n')
    f.close()
    # run application
    app.run()
