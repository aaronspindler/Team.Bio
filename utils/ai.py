from django.conf import settings
from openai import OpenAI

from utils.models import GPTModel

client = OpenAI(api_key=settings.OPENAI_KEY)

try:
    DEFAULT_MODEL = GPTModel.objects.get(primary=True).name
except Exception:
    DEFAULT_MODEL = "gpt-3.5-turbo-16k"


def prompt_gpt(prompt, model=DEFAULT_MODEL, temperature=1.4):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=temperature,
    )
    return completion.choices[0].message.content
