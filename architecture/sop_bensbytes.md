# Ben's Bytes Scraper SOP

## Goal
Extract the latest newsletter content from Ben's Bytes while reliably bypassing Cloudflare TLS security layers.

## Input Constraints
- **Target URL:** `https://www.bensbytes.com/`
- **Bot Protection:** Extremely aggressive Cloudflare. Denies pure Python `requests` at the TLS envelope layer (`TLSV1_ALERT_INTERNAL_ERROR`).

## Execution Logic (Playwright)
1. Initialize a headless Chromium instance via `playwright.sync_api`.
2. Navigate to `https://www.bensbytes.com/`.
3. Wait for the page load event and an additional 3000ms delay to allow Cloudflare's JS challenges to resolve.
4. Extract the full rendered HTML using `page.content()`.
5. Close the browser context to prevent memory leaks.
6. Pass the raw HTML to `BeautifulSoup4`.
7. **Selector Strategy:**
   - Look for the primary article link/header on the homepage.
   - Extract title, URL, and summary.

## Expected Output Structure
Must return a tuple or dict adhering to:
- `source`: "Ben's Bytes"
- `title`: String
- `url`: String
- `summary`: String
- `published_at`: Current UTC ISO timestamp (as proxy)

## Error Handling
- Playwright timeouts generally throw a `TimeoutError`. Catch it, log failure to `progress.md`, and return empty payload.
