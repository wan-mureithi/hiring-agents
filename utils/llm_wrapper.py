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
    print("RESPONSE", response)
    if response.status_code == 200:
        data = response.json()
        print("✅ Model Output:", data.get("response"))
        return data.get("response", "").strip()
        # return response.json().get("response", "").strip()
    else:
        raise RuntimeError(f"Ollama error: {response.status_code} - {response.text}")
