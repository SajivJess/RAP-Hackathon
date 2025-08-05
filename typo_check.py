import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "mistral"

def correct_typo(text):
    prompt = (
        "You are a company name correction assistant.\n"
        "If the following input contains a misspelled or incorrect company name, please correct it.\n"
        "Only reply with the corrected company name. If it's already correct, repeat it as-is.\n\n"
        f"Company name: {text.strip()}"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", text).strip()
    except Exception as e:
        print(f"[ERROR] Company name correction failed: {e}")
        return text  # fallback to original input
