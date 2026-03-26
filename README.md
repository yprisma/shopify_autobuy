# Shopify Restock Bot
**Tools:** Python, Selenium, Pushover API, Pickle  
**Type:** Browser automation / web scraping

---

## Overview
A Python automation tool that monitors a Shopify product page for restocks, automatically completes a purchase the moment inventory becomes available via Shop Pay, and sends a real-time push notification to a phone confirming the order.

Built to solve a problem I had: high-demand Shopify products sell out in seconds, making manual monitoring impractical, especially with a timezone difference. This bot removes the need to watch a page over and over.

Originally built to target the [Formd T1 Titanium](https://formdt1.com).

---

## How It Works

### `cookies.py` — Session Authentication
- Opens a Chrome browser session and navigates to the product page
- Waits for the user to manually log in, then **serializes the authenticated session cookies to disk using `pickle`**
- This means the bot never stores raw credentials — it captures and reuses a live browser session instead

### `formd_web_check.py` — Monitor & Purchase
1. **Loads the saved session** — restores cookies into a new Chrome session so the bot is pre-authenticated
2. **Polls the product page** on a randomized interval (~30–38 minutes) to avoid detection
3. **Checks stock status** by inspecting the `disabled` attribute on the Shop Pay accelerated checkout button via XPath
4. **Executes purchase** — when the button becomes active, clicks through the Shop Pay two-step checkout flow automatically
5. **Sends a push notification** to the user's phone via the **Pushover API** confirming the bot fired

---

## Technical Details
- Uses **Selenium WebDriver** to interact with Shopify's JavaScript-rendered storefront — static scraping tools like BeautifulSoup won't work here since the checkout button state is set dynamically by the browser
- **Cookie-based authentication** via `pickle` avoids re-entering credentials on every run and keeps the session alive across restarts
- **Randomized polling interval** (`randrange(1800, 2300)` seconds) mimics human browsing patterns to reduce the chance of being flagged or rate-limited
- **XPath selectors** target both the Shop Pay wallet button and the confirmation pay button, handling the two-step checkout flow
- **Pushover API** delivers an instant push notification to a mobile device when the purchase fires
- Timestamps every failed stock check to stdout for monitoring (`YYYY-MM-DD HH:MM:SS Not available, refreshing page`)

## Limitations & Known Constraints
- Hardcoded to a single product URL and variant ID
- XPath selectors are tied to Formd's current page structure — Shopify theme updates may break them
- Requires the machine to be running and online to poll
- Randomized interval means there's a window where a restock could be missed between checks

---

## Planned Improvements
- [ ] Config file (YAML/JSON) to set any product URL, variant, and polling interval without editing code
- [ ] Headless Chrome mode for lower resource usage
- [ ] Cloud deployment (AWS EC2 or Raspberry Pi) for 24/7 monitoring without keeping a laptop on
- [ ] Smarter stock detection using the Shopify JSON API (`/products/handle.json`) instead of DOM polling — faster and more reliable
- [ ] Exponential backoff during restocks for faster purchase attempts

---

## What I Learned
Shopify storefronts render checkout button states dynamically via JavaScript, meaning the stock status isn't in the page's HTML source — it only exists after the browser fully renders the page. This made Selenium the right tool over static scraping libraries. Implementing cookie-based session persistence also required understanding how browsers store and replay authentication state, and working with the Pushover API added a real-world integration layer to what would otherwise be a purely local script.
