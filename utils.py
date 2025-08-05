import requests
from bs4 import BeautifulSoup

def get_company_news(company_name):
    query = f"{company_name} latest news"
    url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch news: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.select("a.title")

    news_items = []
    for article in articles[:5]:
        title = article.get_text(strip=True)
        link = article.get("href")
        if title and link and link.startswith("http"):
            news_items.append({"title": title, "link": link})

    return news_items
