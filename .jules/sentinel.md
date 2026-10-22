## 2026-06-28 - [Secure Webhook Secret Validation]
**Vulnerability:** Timing attack vulnerability in webhook secret validation.
**Learning:** Using standard string equality (`!=` or `==`) for comparing secrets allows attackers to perform timing attacks, potentially discovering the secret length and content character by character.
**Prevention:** Always use `hmac.compare_digest` for comparing secrets or tokens (e.g., webhook payloads). Ensure both arguments are validated as strings (not `None`) before passing them to the comparison function.

## 2025-02-14 - Fix Lit innerHTML XSS Vulnerability
**Vulnerability:** The frontend application used Lit templating to bind dynamically generated SVG (from `QRCode.toString`) directly to the `.innerHTML` attribute of a div in `meraki-guest-access-card.ts` and `meraki-wifi-qr-card.ts`. This direct binding bypasses Lit's contextual escaping and DOM management, posing an XSS risk if the string ever contained unsanitized user input (like a malicious SSID).
**Learning:** Directly assigning to `.innerHTML` in lit templates (e.g., `.innerHTML=${...}`) is an anti-pattern. Lit's `unsafeHTML` and `unsafeSVG` directives must be used for explicit parsing and marking of unsafe rendering points.
**Prevention:** Use `unsafeSVG` or `unsafeHTML` from `lit/directives/` and inject it cleanly as text content between the elements (e.g., `> ${unsafeSVG(qrSvg)} </div>`) instead of using `.innerHTML`.

## 2025-02-14 - Secure WebSocket Error Handling
**Vulnerability:** WebSocket API endpoints exposed raw internal exception details by passing `str(err)` directly back to clients in error responses. This violates secure failure principles and risks leaking sensitive backend context.
**Learning:** Exception details must be kept strictly server-side and genericized before transmission to clients.
**Prevention:** Always substitute raw error string details with opaque internal error messages in client-facing API responses while relying on `_LOGGER.exception` for diagnostic tracking server-side.
