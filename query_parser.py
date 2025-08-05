import re

def is_valid_news_query(query: str) -> bool:
    """
    Returns True if the query is related to news about a company/topic.
    Filters out general chit-chat or irrelevant queries.
    """
    query_lower = query.lower().strip()
    news_keywords = ["news", "happened", "about", "incident", "issue", "report", "latest", "update", "trending"]
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    known_companies = ["amazon", "google", "microsoft", "apple", "meta", "facebook", "tesla", "uber", "linkedin", "twitter", "netflix", "adobe", "ibm", "intel", "samsung", "oracle", "walmart", "cisco", "sony", "paypal"]
    # Reject greetings and small talk
    if any(greet == query_lower or greet in query_lower for greet in greetings):
        return False
    # Accept if any news keyword is present
    if any(keyword in query_lower for keyword in news_keywords):
        return True
    # Accept if input is a single word and is a known company name
    if query_lower.isalnum() and ' ' not in query_lower:
        if query_lower in known_companies:
            return True
        else:
            return False
    # Accept if input is a CSV of 1-5 company names (alphanumeric, comma-separated, all must be known)
    if ',' in query:
        parts = [p.strip().lower() for p in query.split(',') if p.strip()]
        if 1 <= len(parts) <= 5 and all(part.replace(' ', '').isalnum() and part in known_companies for part in parts):
            return True
        else:
            return False
    return False


def extract_search_query(query: str) -> str:
    """
    Extract the target company/topic from a natural language query.
    Works for patterns like:
    - 'news about Tesla'
    - 'what happened to Google?'
    - 'latest update about Amazon'
    - 'incident involving Uber'
    """
    known_companies = ["amazon", "google", "microsoft", "apple", "meta", "facebook", "tesla", "uber", "linkedin", "twitter", "netflix", "adobe", "ibm", "intel", "samsung", "oracle", "walmart", "cisco", "sony", "paypal"]
    # Normalize query
    query = query.strip()

    # Try to extract content after keywords
    patterns = [
        r"about ([\w\s&\.-]+)",
        r"to ([\w\s&\.-]+)",
        r"of ([\w\s&\.-]+)",
        r"on ([\w\s&\.-]+)",
        r"for ([\w\s&\.-]+)",
        r"regarding ([\w\s&\.-]+)",
        r"involving ([\w\s&\.-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            # Remove trailing punctuation and whitespace, normalize spaces, and title-case
            name = re.sub(r'[\s\.,!?]+$', '', match.group(1).strip())
            name = re.sub(r'\s+', ' ', name)
            name = name.lower()
            if name in known_companies:
                return name.title()
            else:
                return None

    # Fallback: try to extract last word (case-insensitive, ignore spaces)
    words = re.findall(r'[a-zA-Z0-9&\.-]+', query)
    if words:
        name = words[-1].lower()
        if name in known_companies:
            return name.title()
        else:
            return None
    return None
