from ollama import Client


def setup_client(host):
    return Client(host=f'http://{host}:11434', headers={'Content-Type': 'application/json'})


def list_models(client):
    model_data = client.list()
    models = []
    for m in model_data.models:
        models.append(m.model)
    return models


def ask_model(client, model, prompt):
    response = client.chat(model=model, messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
    return response


def delete_model(client, model):
    client.delete(model)
    print(f'[+] Deleting {model}')


def download_model(client, model):
    print(f'[+] Pulling model: {model}')
    client.pull(model)
