import time

from playwright.sync_api import Page, sync_playwright


def verify_semantic_ui(page: Page):
    url = "http://localhost:8080/index.html"
    page.goto(url)

    # Wait for the script to load and the element to be defined
    page.wait_for_function("customElements.get('meraki-panel') !== undefined")

    # Set mock hass and panel objects to trigger rendering
    page.evaluate("""
        const panel = document.querySelector('meraki-panel');
        panel.hass = {
            states: {
                'switch.living_room_ap': { state: 'on' },
                'switch.office_switch': { state: 'on' },
                'camera.front_door_camera': { state: 'idle' },
                'switch.main_wifi': { state: 'on' }
            },
            themes: { darkMode: false },
            callWS: async (msg) => {
                if (msg.type === 'config_entries/get') return [{ entry_id: 'test_entry' }];
                return {};
            }
        };
        panel.panel = { config: { config_entry_id: 'test_entry' } };
    """)

    # Wait for data to load (App.tsx mock data when hostname is localhost)
    page.wait_for_selector("text=Cisco Meraki Integration", timeout=10000)

    # Take a screenshot of the dashboard
    page.screenshot(path="verification/dashboard.png", full_page=True)

    # Click on a network to open it
    page.click("text=[Network] Main Office")

    # Wait for the network content to appear
    page.wait_for_selector("text=Wireless APs Online", timeout=5000)

    # Take a screenshot of the network view
    page.screenshot(path="verification/network_view.png", full_page=True)

    # Toggle dark mode
    page.evaluate("""
        const panel = document.querySelector('meraki-panel');
        panel.hass = { ...panel.hass, themes: { darkMode: true } };
        document.documentElement.classList.add('dark');
    """)
    time.sleep(1)
    page.screenshot(path="verification/network_view_dark.png", full_page=True)


if __name__ == "__main__":
    import subprocess

    server_process = subprocess.Popen(
        ["python3", "-m", "http.server", "8080"], cwd="custom_components/meraki_ha/www"
    )

    time.sleep(2)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1200})
        try:
            verify_semantic_ui(page)
        except Exception as e:
            print(f"Error during verification: {e}")
            # Try to take an error screenshot if anything is visible
            try:
                page.screenshot(path="verification/error_screenshot.png")
            except:
                pass
        finally:
            browser.close()
            server_process.terminate()
