import requests
import json


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral:7b-instruct"


def call_ollama(prompt):
    """Send a prompt to the local Ollama endpoint and return the response text."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json().get("response", "").strip()


class BaseJudge:

    def __init__(self, name):
        self.name = name

    def evaluate(self, text):
        raise NotImplementedError
