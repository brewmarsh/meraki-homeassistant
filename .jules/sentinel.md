## 2026-06-28 - [Secure Webhook Secret Validation]
**Vulnerability:** Timing attack vulnerability in webhook secret validation.
**Learning:** Using standard string equality (`!=` or `==`) for comparing secrets allows attackers to perform timing attacks, potentially discovering the secret length and content character by character.
**Prevention:** Always use `hmac.compare_digest` for comparing secrets or tokens (e.g., webhook payloads). Ensure both arguments are validated as strings (not `None`) before passing them to the comparison function.## 2025-02-14 - Fix Lit innerHTML XSS Vulnerability
**Vulnerability:** The frontend application used Lit templating to bind dynamically generated SVG (from \`QRCode.toString\`) directly to the \`.innerHTML\` attribute of a div in \`meraki-guest-access-card.ts\` and \`meraki-wifi-qr-card.ts\`. This direct binding bypasses Lit's contextual escaping and DOM management, posing an XSS risk if the string ever contained unsanitized user input (like a malicious SSID).
**Learning:** Directly assigning to \`.innerHTML\` in lit templates (e.g., \`.innerHTML=\${...}\`) is an anti-pattern. Lit's \`unsafeHTML\` and \`unsafeSVG\` directives must be used for explicit parsing and marking of unsafe rendering points.
**Prevention:** Use \`unsafeSVG\` or \`unsafeHTML\` from \`lit/directives/\` and inject it cleanly as text content between the elements (e.g., \`> \${unsafeSVG(qrSvg)} </div>\`) instead of using \`.innerHTML\`.
## 2026-10-17 - [Prevent Information Leakage in WebSocket Error Responses]
**Vulnerability:** The WebSocket API directly returned raw exception strings (`str(err)`) to the client when an error occurred (e.g., in `ws_create_guest_key`, `ws_subscribe_meraki_data`, and the generic `handle_ws_error` wrapper). This risks leaking sensitive information such as stack traces, file paths, or internal API details to the client.
**Learning:** In WebSocket error responses (e.g., `connection.send_error()`), never leak raw exception strings (`str(err)`) to the client, as this can expose stack traces and internal API details.
**Prevention:** Always log the exception server-side and send a generic, safe error message (e.g., "An unexpected error occurred") to the client to ensure secure failure.
## 2026-06-28 - [Fix Test Overrides for CI Passes]
**Vulnerability:** Tests failed on properties asserting MagicMock methods due to previous state mismatches.
**Learning:** The CI pipeline will fail if modified code causes previous state changes in mocked tests. Even if the code you write is correct, you should always fix existing bugs in tests to pass the pipeline.
**Prevention:** Before making code changes in test directories, run the target tests. When modifying tests or code that affects test state, verify the impact locally and ensure that all mocked states remain aligned with expected values.
