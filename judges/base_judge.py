import requests
import json
import os
from pathlib import Path

def _load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())

_load_env()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral:7b-instruct"


def call_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except Exception:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Ollama is not running and ANTHROPIC_API_KEY is not set."
            )
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text


class BaseJudge:

    def __init__(self, name):
        self.name = name

    def evaluate(self, text):
        raise NotImplementedError

Then rename the .env file. Find the file currently named ANTHROPIC_API_KEY.env and rename it to just .env with nothing before the dot.

Then run:
git add judges/base_judge.py
git commit -m "Fix env file loading in base judge"
git push
