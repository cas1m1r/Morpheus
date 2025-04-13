import os

import requests
import pyttsx3
import json
import sys


def ask_model(prompt, url, model):
    reply = ''
    completed = False
    prompt_heading = (f'You are a helpful assistant that answers with *brief* straightforward answers. '
                    f'You are also sarcastic and witty. Overall you are a fun companion that tries to provide '
                    f'simple and entertaining answers to questions.\n'
                    f'### Instruction:\n{prompt}\n### Response:\n')
    question = {"model": model, "messages": [{"role": "user", "content": prompt_heading + prompt}]}
    api = requests.post(url, json=question)
    # While loop accumulating reply data until "finished"
    while not completed:
        latest_data = api.text
        # look for completed or termination data
        for line in latest_data.splitlines():
            api_data = json.loads(line)
            completed = api_data['done']
            if not state:
                reply += remove(remove(api_data['message']['content'],'#'), '*')
    print(reply)
    return reply


def remove(s: str, token: str):
    return s.replace(token, '')


def assistant(prompt, model):
    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty("volume", 0.6)
    # Ask prompt
    result = ask_model(prompt, url, model)
    print(prompt)
    engine.say(result.split('</think>')[-1])
    engine.runAndWait()
    return result


def main():
    model = "gemma3:1b"
    url = 'http://127.0.0.1:11343/api/chat'
    # Get a prompt
    if len(sys.argv) > 1:
        prompt = ' '.join(sys.argv[2:])
    else:
        print(f'[X] Usage: {sys.argv[0]} [prompt]')
        exit()
    load_dotenv()
    if 'URL' in os.environ.keys():
        url = os.environ['URL']
    if 'MODEL' in os.environ.keys():
        model = os.environ['MODEL']
    assistant(prompt, url, model)


if __name__ == '__main__':
    main()
