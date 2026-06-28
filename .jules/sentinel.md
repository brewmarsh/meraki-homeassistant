## 2026-06-28 - [Secure Webhook Secret Validation]
**Vulnerability:** Timing attack vulnerability in webhook secret validation.
**Learning:** Using standard string equality (`!=` or `==`) for comparing secrets allows attackers to perform timing attacks, potentially discovering the secret length and content character by character.
**Prevention:** Always use `hmac.compare_digest` for comparing secrets or tokens (e.g., webhook payloads). Ensure both arguments are validated as strings (not `None`) before passing them to the comparison function.