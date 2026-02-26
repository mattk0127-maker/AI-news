import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import hashlib

def extract():
    """Extracts the latest article from The AI Rundown."""
    url = "https://therundown.ai/"
    result = {
        "success": False,
        "article": None,
        "error": None
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Heuristic extraction since we don't know the exact class names.
        # Find the first prominent link or use the page meta tags if there isn't a clear "latest post" feed.
        
        title_tag = soup.find('h1') or soup.find('h2')
        title = title_tag.get_text(strip=True) if title_tag else soup.title.string.replace('Home | ', '')
        
        # Since we are scraping the landing page, we'll try to find a link that looks like an article.
        link_tag = soup.find('a', href=lambda href: href and ('/post/' in href or '/p/' in href))
        article_url = url
        if link_tag and 'href' in link_tag.attrs:
             article_url = link_tag['href']
             if not article_url.startswith('http'):
                 article_url = url.rstrip('/') + '/' + article_url.lstrip('/')

        # Look for a paragraph for the summary
        p_tag = soup.find('p')
        summary = p_tag.get_text(strip=True) if p_tag else "Latest news and updates from The AI Rundown."
        
        # Limit summary length
        if len(summary) > 200:
            summary = summary[:197] + "..."

        published_at = datetime.utcnow().isoformat()
        
        # Generate stable ID
        raw_id = f"The AI Rundown_{title}"
        article_id = hashlib.md5(raw_id.encode('utf-8')).hexdigest()

        result["article"] = {
            "id": article_id,
            "source": "The AI Rundown",
            "title": title,
            "url": article_url,
            "summary": summary,
            "published_at": published_at,
            "is_saved": False
        }
        result["success"] = True

    except Exception as e:
        result["error"] = str(e)
        
    return result

if __name__ == "__main__":
    print(json.dumps(extract(), indent=2))
