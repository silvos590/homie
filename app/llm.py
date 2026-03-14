import httpx

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.1:8b-instruct-q4_K_M"

def ask(system_prompt: str, user_message: str) -> str:
    response = httpx.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message}
            ]
        },
        timeout=60.0  # Pi can be slow on first token
    )
    return response.json()["message"]["content"]