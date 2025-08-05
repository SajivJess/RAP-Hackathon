import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def summarize_news(news_items, style="Formal business summary"):
    """
    Summarize news using local Mistral 7B model via Ollama API.
    Args:
        news_items (list): List of news dicts with 'title', 'link', and optionally 'text'.
        style (str): Output style.
    Returns:
        str: Summary string from LLM.
    """
    if not news_items:
        return "No news items to summarize."

    prompt = f"Summarize the following news in the style: {style}.\n\n"
    for i, item in enumerate(news_items, 1):
        prompt += f"{i}. {item.get('title', '')}\n"
        if item.get('link'):
            prompt += f"   Link: {item['link']}\n"
        if item.get('text'):
            # Add a snippet of the article text (limit to 1000 chars for prompt size)
            snippet = item['text'][:1000] + ('...' if len(item['text']) > 1000 else '')
            prompt += f"   Article: {snippet}\n"
    prompt += "\nSummary:"

    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "[No summary returned]")
    except Exception as e:
        return f"[Error contacting Ollama Mistral: {e}]"
