import sys
import os

import openai
from openai.error import APIError
from dotenv import load_dotenv

load_dotenv()

model = "text-davinci-003"
MAX_TOK = 4096  # davinci has 4096 context tokens
MIN_TOK = 128 # minimal tokens we allow
api_key = os.getenv('OPENAI_API_KEY')
assert api_key
openai.api_key = api_key

# about four characters per token

# XXX: how many chars should be read?
# Some endpoints have a shared maximum of 2048 tokens
# prompt tokens plus max_tokens cannot exceed the model's context length

# don't read prompts longer than half the context length
prompt = sys.stdin.read(MAX_TOK // 2 * 4)
#prompt = open('').read()

# XXX: print warning if input was truncated?

n_prompt_tokens = len(prompt) // 4

# XXX: assume we want to cap output at max X times the input prompt length
# I don't know which proportion is right

n_tokens = min(MAX_TOK, 3 * n_prompt_tokens + MIN_TOK)

try:
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0,
        max_tokens=n_tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
except APIError as e:
    sys.stdout.close()
    raise e
else:
    print(response['choices'][0]['text'])
