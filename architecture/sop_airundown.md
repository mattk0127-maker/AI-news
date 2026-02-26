# AI Rundown Scraper SOP

## Goal
Extract the latest daily newsletter from The AI Rundown website deterministically.

## Input Constraints
- **Target URL:** `https://therundown.ai/`
- **Rate Limits:** Unknown, but assumes basic scraping limits. A single daily hit is entirely safe.
- **Bot Protection:** The site responds with a 200 OK simply by having a standard `User-Agent` header set.

## Execution Logic (BeautifulSoup)
1. Initialize a Python `requests` session with a Chrome `User-Agent`.
2. Fetch `https://therundown.ai/`.
3. Check for Status 200. If != 200, log error and exit.
4. Parse the HTML using `BeautifulSoup4`.
5. **Selector Strategy:** 
   - We need to extract the title, URL, summary, and date of the most recent article on the homepage.
   - *Because actual selectors might change over time, we use a heuristic approach looking for `<a>` tags with large text or specific classes indicative of recent news.*
6. For safety, extract the `soup.title.string` and generic `h1`/`h2` text if specific article elements aren't immediately found.

## Expected Output Structure
Must return a tuple or dict adhering to:
- `source`: "The AI Rundown"
- `title`: String
- `url`: String
- `summary`: String (first paragraph or meta description)
- `published_at`: Current UTC ISO timestamp (as proxy if not found in HTML)

## Error Handling
- If `requests.get` timeouts: Retry once after 5s. If fails again, return empty payload structure and `SUCCESS: False`.
