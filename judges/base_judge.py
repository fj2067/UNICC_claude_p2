import requests
import json
import os

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
                "Ollama is not running and ANTHROPIC_API_KEY is not set.\n"
                "Option 1 - Local: ollama serve\n"
                "Option 2 - API: export ANTHROPIC_API_KEY=your_key_here"
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
