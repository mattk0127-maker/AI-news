from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import json
import hashlib

def extract():
    """Extracts the latest article from Ben's Bytes using a Chromium browser to bypass Cloudflare."""
    url = "https://www.bensbytes.com/"
    result = {
        "success": False,
        "article": None,
        "error": None
    }
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            page = context.new_page()
            
            # Go to page and wait for it to fully load + wait 3s for Cloudflare JS to pass
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(3000) 
            
            html = page.content()
            browser.close()
            
            # Parse the extracted HTML
            soup = BeautifulSoup(html, 'html.parser')
            
            # Heuristic extraction
            title_tag = soup.find('h1') or soup.find('h2')
            title = title_tag.get_text(strip=True) if title_tag else soup.title.string
            
            link_tag = soup.find('a', href=lambda href: href and ('/p/' in href or '/post/' in href))
            article_url = url
            if link_tag and 'href' in link_tag.attrs:
                 article_url = link_tag['href']
                 if not article_url.startswith('http'):
                     article_url = url.rstrip('/') + '/' + article_url.lstrip('/')
                     
            p_tag = soup.find('p')
            summary = p_tag.get_text(strip=True) if p_tag else "The daily AI newsletter."
            
            if len(summary) > 200:
                summary = summary[:197] + "..."
                
            published_at = datetime.utcnow().isoformat()
            
            # Generate stable ID
            raw_id = f"Ben's Bytes_{title}"
            article_id = hashlib.md5(raw_id.encode('utf-8')).hexdigest()

            result["article"] = {
                "id": article_id,
                "source": "Ben's Bytes",
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
