import sys
from playwright.sync_api import sync_playwright

APPS = [
    "https://airline-route-profitability.streamlit.app",
    "https://pharmaverse-clinical-dashboard.streamlit.app/",
    "https://insurance-fraud-detection-4jqywawedpwrfsdxcwlryt.streamlit.app/",
    "https://mental-health-risk-profile.streamlit.app/",
  "https://nopd-calls-for-service.streamlit.app/", "https://learning-hindi.streamlit.app/",
    "https://cihi-cancer-readmission.streamlit.app/",
]



def visit(page, url):
    print(f"Visiting {url}")
    page.goto(url, wait_until="networkidle", timeout=60000)
    try:
        btn = page.get_by_text("Yes, get this app back up!", exact=False)
        if btn.is_visible(timeout=5000):
            btn.click()
            print("  -> was asleep, clicked wake button")
            page.wait_for_timeout(15000)
            page.wait_for_load_state("networkidle", timeout=60000)
    except Exception:
        print("  -> already awake")

    # Sanity check: make sure the app actually rendered, not stuck on an error/sleep page
    page.wait_for_timeout(3000)
    body = page.inner_text("body").lower()
    if "get this app back up" in body or "oh no" in body or "error running app" in body:
        raise RuntimeError("app did not wake / showed an error page")

def main():
    failures = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in APPS:
            try:
                visit(page, url)
                print("  OK")
            except Exception as e:
                print(f"  !! FAILED: {url} -> {e}")
                failures.append(url)
        browser.close()

    if failures:
        print("\n=== FAILED APPS ===")
        for url in failures:
            print(url)
        sys.exit(1)   # non-zero exit -> workflow fails -> GitHub emails you
    print("\nAll apps awake.")

if __name__ == "__main__":
    main()
