from playwright.sync_api import sync_playwright
import traceback

print("Starting verification script...")
try:
    with sync_playwright() as p:
        print("Playwright started.")
        browser = p.chromium.launch(headless=True)
        print("Browser launched.")
        page = browser.new_page()
        print("New page created.")
        page.goto("http://localhost:9999/")
        print("Navigated to page.")
        page.screenshot(path="/app/verification.png")
        print("Screenshot taken.")
        browser.close()
        print("Browser closed.")
except Exception as e:
    print("An error occurred:")
    traceback.print_exc()
print("Verification script finished.")
