import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'dashboard', '.env'))

def get_airundown_articles():
    url = "https://therundown.ai/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("Fetching The AI Rundown homepage...")
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, 'html.parser')
    
    articles = []
    
    # Attempt to find all cards
    # Beehiiv standard structure wraps the posts in a tags, usually containing headers
    links = soup.find_all('a', href=True)
    
    seen_urls = set()
    
    for link in links:
        href = link['href']
        if '/p/' not in href and '/post/' not in href:
            continue
            
        full_url = href if href.startswith('http') else url.rstrip('/') + '/' + href.lstrip('/')
        
        if full_url in seen_urls:
            continue
            
        # Try to find a heading inside the link block or near it
        title_block = link.find(['h2', 'h3'])
        if not title_block:
            # Maybe the text itself is prominent?
            text = link.get_text(strip=True)
            if len(text) < 10 or len(text) > 300: # Not a title
                continue
            title = text.split('PLUS:')[0].strip()
            summary = text.replace(title, '').strip()
            if not summary:
                summary = "Latest updates from The AI Rundown."
        else:
            title = title_block.get_text(strip=True)
            # Find the paragraph below it
            p_block = link.find('p')
            summary = p_block.get_text(strip=True) if p_block else "Latest updates from The AI Rundown."
            
        seen_urls.add(full_url)
        
        raw_id = f"The AI Rundown_{title}"
        article_id = hashlib.md5(raw_id.encode('utf-8')).hexdigest()

        articles.append({
            "id": article_id,
            "source": "The AI Rundown",
            "title": title,
            "url": full_url,
            "summary": summary,
            "published_at": datetime.utcnow().isoformat(),
            "is_saved": False
        })
        
        if len(articles) >= 20: # We want 20 max
            break
            
    print(f"Extracted {len(articles)} articles!")
    return articles

def seed_data():
    supabase_url = os.environ.get("VITE_SUPABASE_URL")
    supabase_key = os.environ.get("VITE_SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("Missing Supabase credentials!")
        return

    articles = get_airundown_articles()
    
    if not articles:
        print("No articles found to push.")
        return

    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    endpoint = f"{supabase_url}/rest/v1/articles"
    
    # First, let's optionally DELETE all existing articles to give a clean slate for the UI 
    # (so we don't mix fake AI Valley posts with real ones)
    print("Clearing old seeded articles...")
    try:
         requests.delete(endpoint, headers=headers, params={"id": "not.eq.0"})
    except:
         pass

    print(f"Pushing {len(articles)} real articles to Supabase...")
    try:
        response = requests.post(endpoint, headers=headers, json=articles)
        response.raise_for_status()
        print("Successfully seeded real data to Supabase!")
    except Exception as e:
        print(f"Failed to push to Supabase: {e}")
        if hasattr(e, 'response') and e.response:
             print(e.response.text)

if __name__ == "__main__":
    seed_data()
