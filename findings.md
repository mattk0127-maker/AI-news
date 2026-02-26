# Findings

## Research
- Initial target sources for scraping: **Ben's Bytes**, **The AI Rundown**, and possibly **Reddit**.
- Need to research the HTML structure of these websites to build specific parser tools.

## Discoveries & Constraints
- **Scraping Block:** Ben's Bytes (`bensbytes.com`) aggressively blocks both basic Python `requests` and `Playwright Chromium` at the TLS envelope layer (`TLSV1_ALERT_INTERNAL_ERROR` / `net::ERR_SSL_PROTOCOL_ERROR`). A commercial scraping API (like ZenRows or BrightData) is necessary for this specific target.
- **Scraping Success:** The AI Rundown returns a clean 200 OK with a basic User-Agent string. 
- **North Star:** Build a beautiful interactive dashboard that collects and displays articles from the last 24 hours.
- **Integrations:** Scraping scripts initially. Supabase integration planned for later.
- **Source of Truth:** Scraped website data (eventually moving to Supabase).
- **Delivery Payload:** Clean JSON payload delivered to a gorgeous UI, capable of showing daily changes and maintaining a 'saved' state for individual articles.
