from playwright.sync_api import sync_playwright, Page, expect
import traceback

def run_test():
    with sync_playwright() as p:
        try:
            print("Launching browser")
            browser = p.chromium.launch()
            page = browser.new_page()
            print("Starting test_new_ui")

            print("Navigating to http://localhost:5174")
            page.goto("http://localhost:5174", timeout=60000) # Increased timeout
            print("Navigation complete")

            # Give the page some time to load completely
            page.wait_for_load_state('networkidle')

            print("Taking screenshot to verification.png")
            page.screenshot(path="/app/jules-scratch/verification/verification.png")
            print("Screenshot taken")

            browser.close()
            print("Finished test_new_ui")

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    run_test()
