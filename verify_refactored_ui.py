import asyncio
import http.server
import os
import socketserver
import threading

from playwright.async_api import async_playwright

PORT = 8080


async def main():
    """Verify the UI."""
    os.chdir("custom_components/meraki_ha/www")

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True

    try:
        server_thread.start()
        print(f"Serving at port {PORT}")

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

<<<<<<< HEAD
            await page.goto(f"http://localhost:{PORT}")

            # Mock the hass object
            await page.evaluate("""
=======
            page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))

            await page.goto(f"http://localhost:{PORT}")

            # Mock the hass object
            await page.evaluate(
                """
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
                window.hass = {
                  connection: {
                    sendMessagePromise: async (message) => {
                      console.log('Mock sendMessagePromise called with:', message);
                      return Promise.resolve({
                        networks: [
                            { id: 'net-1', name: 'Marshmallow Home' },
                            { id: 'net-2', name: 'Shenanibarn' }
                        ],
                        devices: [
                          {
                            networkId: 'net-1',
                            name: 'Living Room AP',
                            model: 'MR33',
                            serial: 'Q2JD-XXXX-YYYY',
                            status: 'online',
                            lanIp: '192.168.1.1'
                          },
                          {
                            networkId: 'net-2',
                            name: 'Barn Camera',
                            model: 'MV12',
                            serial: 'Q2LD-XXXX-ZZZZ',
                            status: 'online',
                            lanIp: '10.0.0.1'
                          },
                        ],
                      });
                    }
                  },
                  themes: {
                    darkMode: true,
                  },
                };
<<<<<<< HEAD
            """)

            await page.evaluate("""
=======
            """
            )

            await page.evaluate(
                """
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
                const el = document.createElement('meraki-panel');
                el.hass = window.hass;
                el.panel = {
                    config: {
                        config_entry_id: 'mock-entry-id'
                    }
                }
                document.body.appendChild(el);
<<<<<<< HEAD
            """)

            page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))

            print("Waiting for selector...")
            await page.wait_for_selector('text="Meraki Integration Control"')
=======
            """
            )

            print("Waiting for selector...")
            await page.wait_for_selector('text="Meraki HA Web UI"')
>>>>>>> ea81ca1 (Merge pull request #851 from brewmarsh/chore/fix-test-dependencies-18300066891703763116)
            print("Selector found!")

            screenshot_path = "verification_screenshot.png"
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            await browser.close()

    finally:
        httpd.shutdown()
        server_thread.join()
        os.chdir("../../..")


if __name__ == "__main__":
    asyncio.run(main())
