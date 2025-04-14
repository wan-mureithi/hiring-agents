import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"


def query_llm(prompt: str, system_prompt: str = "") -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
        },
    )

    if response.status_code == 200:
        return response.json().get("response", "").strip()
    else:
        raise RuntimeError(f"Ollama error: {response.status_code} - {response.text}")
