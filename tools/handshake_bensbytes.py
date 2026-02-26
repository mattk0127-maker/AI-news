import requests
from bs4 import BeautifulSoup

def handshake():
    url = "https://www.bensbytes.com/"
    print(f"Attempting handshake with {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title Found"
            print(f"Page Title: {title}")
            print("Handshake: SUCCESS")
        else:
            print("Handshake: FAILED (Non-200 Status)")
            
    except Exception as e:
        print(f"Handshake error: {e}")

if __name__ == "__main__":
    handshake()
