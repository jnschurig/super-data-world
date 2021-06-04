import os, json
import openai

script_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(script_path, 'openai_credentials.json'), 'r', encoding='utf-8') as f:
    openai_creds = json.load(f)

openai.api_key = openai_creds['apikey']

response = openai.Completion.create(engine="davinci", prompt="This is a test", max_tokens=10)

print(response)
