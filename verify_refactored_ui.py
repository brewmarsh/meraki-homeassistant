import asyncio
import http.server
import os
import socketserver
import threading

from playwright.async_api import async_playwright

PORT = 8085


async def main():
    """Verify the UI."""
    # We will serve the current directory, but we need to find where we are.
    # The script is in the root.
    repo_root = os.getcwd()
    www_dir = os.path.join(repo_root, "custom_components", "meraki_ha", "www")

    # Change to www dir to serve files from there
    os.chdir(www_dir)

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

            page.on("console", lambda msg: print(f"Browser Console: {msg.text}"))
            page.on("pageerror", lambda err: print(f"Page Error: {err}"))

            # Route requests for the JS file to the correct location
            # HTML asks for /local/meraki_ha/meraki-panel.js
            # We want to serve /meraki-panel.js (relative to www root)
            await page.route(
                "**/local/meraki_ha/meraki-panel.js",
                lambda route: route.fulfill(
                    path=os.path.join(www_dir, "meraki-panel.js")
                ),
            )

            await page.goto(f"http://localhost:{PORT}")

            # Mock the hass object
            await page.evaluate("""
                window.hass = {
                  connection: {
                    subscribeMessage: (callback, options) => {
                      console.log('Mock subscribeMessage called with:', options);
                      const mockData = {
                        org_name: 'Mock Organization',
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
                            lanIp: '192.168.1.1',
                            productType: 'wireless'
                          },
                          {
                            networkId: 'net-2',
                            name: 'Barn Camera',
                            model: 'MV12',
                            serial: 'Q2LD-XXXX-ZZZZ',
                            status: 'online',
                            lanIp: '10.0.0.1',
                            productType: 'camera'
                          },
                        ],
                        clients: [
                            { description: 'My Phone', ip: '192.168.1.50' }
                        ]
                      };

                      // Simulate async data arrival
                      callback(mockData);

                      return Promise.resolve(() => console.log('Unsubscribed'));
                    }
                  },
                  themes: {
                    darkMode: true,
                  },
                };
            """)

            # The index.html already contains <meraki-panel>
            # but it doesn't have hass set.
            # We can select the existing one and set properties.
            await page.evaluate(
                """
                const el = document.querySelector('meraki-panel');
                if (el) {
                    el.hass = window.hass;
                    el.panel = {
                        config: {
                            config_entry_id: 'mock-entry-id'
                        }
                    }
                } else {
                    console.error('meraki-panel element not found in DOM');
                    const newEl = document.createElement('meraki-panel');
                    newEl.hass = window.hass;
                    newEl.panel = {
                        config: {
                            config_entry_id: 'mock-entry-id'
                        }
                    }
                    document.body.appendChild(newEl);
                }
            """
            )

            print("Waiting for selector...")
            await page.wait_for_selector('text="Meraki Dashboard"')
            print("Selector found!")

            # Wait a bit for data to render (since mock is fast but async)
            await page.wait_for_timeout(500)

            screenshot_path = os.path.join(repo_root, "verification_screenshot.png")
            await page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            await browser.close()

    finally:
        httpd.shutdown()
        server_thread.join()
        os.chdir(repo_root)


if __name__ == "__main__":
    asyncio.run(main())
