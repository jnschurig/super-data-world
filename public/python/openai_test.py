import os, json
import openai

script_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(script_path, 'openai_credentials.json'), 'r', encoding='utf-8') as f:
    openai_creds = json.load(f)

openai.api_key = openai_creds['apikey']

prompt_val = 'alttpr is'

response = openai.Completion.create(engine="davinci", prompt="alttpr is", max_tokens=20, stop='\n')

full_completion = prompt_val + response['choices'][0]['text']

print(response)

print(full_completion)

