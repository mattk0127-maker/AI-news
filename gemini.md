# Project Constitution

## 1. Data Schemas
*Input/Output payload shapes.*

### Input JSON Schema (Raw Scraped Article)
```json
{
  "source": "string", // e.g., "Ben's Bytes", "The AI Rundown"
  "title": "string",
  "url": "string",
  "summary": "string",
  "published_at": "string (ISO 8601)",
  "content_html": "string (optional)"
}
```

### Output JSON Schema (Payload for Dashboard)
```json
{
  "articles": [
    {
      "id": "string (unique hash)",
      "source": "string",
      "title": "string",
      "url": "string",
      "summary": "string",
      "published_at": "string",
      "is_saved": "boolean (Default: false)"
    }
  ],
  "last_synced_at": "string (ISO 8601)"
}
```

## 2. Behavioral Rules
- **UI/UX:** The dashboard MUST be gorgeous, highly interactive, and use the specified brand design guidelines:
  - **Colors:** Primary/Accent: `#E9554D`, Background: `#FFFFFF`, Text Primary: `#222222`, Link: `#3898EC`.
  - **Typography:** `Suisseworks` for headings (h1/h2 at 45px) and `Suisseintl` for body text (16px).
  - Use `LOGO.png` and reference `DesignInspo.png` for layout aesthetics. Visual excellence and premium feel are a strict priority.
- **Logic:** Data fetching must occur every 24 hours. If there's new data, show it; if not, ignore.
- **Persistence:** Saved articles must persist across page refreshes (via LocalStorage initially, Supabase later).
- **Core:** No guessing at business logic; logic must be deterministic.

## 3. Architectural Invariants
- **Layer 1 (Architecture):** SOPs dictate logic. Any change in logic updates SOPs first.
- **Layer 2 (Navigation):** Routing data between Tools.
- **Layer 3 (Tools):** Deterministic Python scripts for scraping and data processing.
- Initially, use local web scrapers. Later, integrate with Supabase as the Source of Truth.

## 4. Maintenance Log
- **2026-02-24:** Project initialized. Discovery questions answered. Data schemas drafted.
- **2026-02-25:** Phase 2, 3, 4, 5 complete.
  - **Architecture:** Layered orchestrator built (`tools/orchestrator.py`) merging results via REST POST into Supabase. 
  - **Tools:** The AI Rundown scraped successfully. Ben's Bytes is severely blocked by Cloudflare TLS checking; Playwright bypass failed. Target extraction set to ~20 valid articles going forward.
  - **Automation:** `tools/trigger.py` configured for a continuous 24-hour polling loop.
  - **Stylize:** React Dashboard reading/writing `is_saved` state directly to the Supabase database, styled purely in `index.css` with primary brand tokens (`#E9554D`, `Suisseintl`).
