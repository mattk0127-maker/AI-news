import os
import json
import hashlib
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import random

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'dashboard', '.env'))

def seed_data():
    supabase_url = os.environ.get("VITE_SUPABASE_URL")
    supabase_key = os.environ.get("VITE_SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        print("Missing credentials")
        return

    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    endpoint = f"{supabase_url}/rest/v1/articles"

    sources = ["The AI Rundown", "Ben's Bytes", "AI Valley", "Prompt Engineering Daily"]
    topics = ["OpenAI", "Anthropic", "Midjourney", "Google Gemini", "Meta LLaMA", "AI Agents", "Coding Copilots"]
    actions = ["releases new update", "crushes benchmarks", "launches enterprise tier", "shows impressive capabilities", "changes pricing"]

    articles = []

    for i in range(20):
        source = random.choice(sources)
        topic = random.choice(topics)
        action = random.choice(actions)
        title = f"{topic} {action}"
        
        summary = f"Summary: {title}. This is a seeded article demonstrating the capabilities of the news aggregator dashboard. We are expecting a lot of exciting things from {topic} this year."
        
        # random date in the last 7 days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        published_at = (datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)).isoformat()
        
        url = "https://example.com"

        raw_id = f"{source}_{title}_{i}"
        article_id = hashlib.md5(raw_id.encode('utf-8')).hexdigest()

        articles.append({
            "id": article_id,
            "source": source,
            "title": title,
            "url": url,
            "summary": summary,
            "published_at": published_at,
            "is_saved": random.choice([True, False, False, False]) # 25% chance to be saved
        })

    print(f"Pushing {len(articles)} mock articles to Supabase...")
    try:
        response = requests.post(endpoint, headers=headers, json=articles)
        response.raise_for_status()
        print("Successfully seeded data to Supabase!")
    except Exception as e:
        print(f"Failed to push to Supabase: {e}")
        if hasattr(e, 'response') and e.response:
             print(e.response.text)

if __name__ == "__main__":
    seed_data()
