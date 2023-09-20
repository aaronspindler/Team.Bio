import openai
from django.conf import settings

from utils.models import GPTModel

openai.api_key = settings.OPENAI_KEY

try:
    DEFAULT_MODEL = GPTModel.objects.get(primary=True).name
except GPTModel.DoesNotExist:
    DEFAULT_MODEL = "gpt-3.5-turbo-16k"


def prompt_gpt(prompt, model=DEFAULT_MODEL, temperature=1.4):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        stream=True,
    )
    collected_messages = []
    for chunk in completion:
        chunk_message = chunk["choices"][0]["delta"]
        if chunk_message == {}:
            break
        collected_messages.append(chunk_message)
        print(chunk_message)
    return "".join([m.get("content", "") for m in collected_messages])
