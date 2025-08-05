import requests
from bs4 import BeautifulSoup
import tempfile
import os
try:
    from newspaper import Article
except ImportError:
    Article = None
try:
    import trafilatura
except ImportError:
    trafilatura = None

def get_news(company):
    query = f"{company} latest news"
    url = f"https://www.bing.com/news/search?q={query.replace(' ', '+')}&FORM=HDRSC6"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch Bing News: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.select("a.title")

    news_list = []
    for article in articles:
        if len(news_list) >= 3:
            break
        title = article.get_text(strip=True)
        link = article.get("href")
        if not (title and link and link.startswith("http")):
            continue
        article_text = ""
        # 1. Try BeautifulSoup
        try:
            art_resp = requests.get(link, headers=headers, timeout=15)
            art_resp.raise_for_status()
            art_soup = BeautifulSoup(art_resp.text, 'html.parser')
            paragraphs = art_soup.find_all('p')
            article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            if len(article_text) < 200:
                raise ValueError("BS4 content too short")
        except Exception as e:
            print(f"[ERROR] BS4 failed: {e}")
        # 2. Try newspaper3k if BS4 fails or is too short
        if (not article_text or len(article_text) < 200) and Article is not None:
            try:
                news_article = Article(link)
                news_article.download()
                news_article.parse()
                article_text = news_article.text
                if len(article_text) < 200:
                    raise ValueError("newspaper3k content too short")
            except Exception as e:
                print(f"[ERROR] newspaper3k failed: {e}")
        # 3. Try trafilatura if both above fail
        if (not article_text or len(article_text) < 200) and trafilatura is not None:
            try:
                downloaded = trafilatura.fetch_url(link)
                if downloaded:
                    article_text = trafilatura.extract(downloaded)
            except Exception as e:
                print(f"[ERROR] trafilatura failed: {e}")
        # Only add if we have usable text
        if article_text and len(article_text) > 100:
            with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.txt') as tf:
                tf.write(article_text)
                temp_path = tf.name
            news_list.append({"title": title, "link": link, "file": temp_path, "text": article_text})
    return news_list
