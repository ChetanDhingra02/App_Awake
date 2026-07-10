from playwright.sync_api import sync_playwright

APPS = [
    "https://airline-route-profitability.streamlit.app",
    "https://pharmaverse-clinical-dashboard.streamlit.app/",
    "https://insurance-fraud-detection-4jqywawedpwrfsdxcwlryt.streamlit.app/",
    "https://mental-health-risk-profile.streamlit.app/",
  "https://nopd-calls-for-service.streamlit.app/",
]

def visit(page, url):
    print(f"Visiting {url}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    # If the app is asleep, click the wake button
    try:
        btn = page.get_by_text("Yes, get this app back up!", exact=False)
        if btn.is_visible(timeout=5000):
            btn.click()
            print("  -> was asleep, clicked wake button")
            page.wait_for_timeout(15000)
    except Exception:
        print("  -> already awake")
    page.wait_for_timeout(3000)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in APPS:
            try:
                visit(page, url)
            except Exception as e:
                print(f"  !! error on {url}: {e}")
        browser.close()

if __name__ == "__main__":
    main()
