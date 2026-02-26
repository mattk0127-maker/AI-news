import json
import os
from datetime import datetime
import requests
from scraper_airundown import extract as extract_airundown
from scraper_bensbytes import extract as extract_bensbytes
from dotenv import load_dotenv

load_dotenv()

def generate_payload():
    """Layer 2 reasoning script. Coordinates tools and compiles the final Payload."""
    print("--- Starting B.L.A.S.T. Orchestrator ---")
    
    articles = []
    
    # 1. AI Rundown
    print("Scraping The AI Rundown...")
    res_ai = extract_airundown()
    if res_ai["success"] and res_ai["article"]:
        articles.append(res_ai["article"])
        print(" -> Success.")
    else:
        print(f" -> Failed: {res_ai.get('error')}")
        
    # 2. Ben's Bytes
    print("Scraping Ben's Bytes...")
    res_bens = extract_bensbytes()
    if res_bens["success"] and res_bens["article"]:
        articles.append(res_bens["article"])
        print(" -> Success.")
    else:
        print(f" -> Failed: {res_bens.get('error')}")

    if not articles:
        print("No articles extracted. Exiting.")
        return

    # Push to Supabase via direct REST API
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("ERROR: Supabase credentials not found in environment.")
        return

    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    endpoint = f"{supabase_url}/rest/v1/articles"
    
    print(f"Pushing {len(articles)} articles to Supabase...")
    try:
        response = requests.post(endpoint, headers=headers, json=articles)
        response.raise_for_status()
        print("Successfully upserted data to Supabase.")
    except Exception as e:
        print(f"Failed to push to Supabase: {e}")
        if hasattr(e, 'response') and e.response:
             print(e.response.text)

if __name__ == "__main__":
    generate_payload()
