# Changelog

## [2.5.1] - 2026-04-08

### Fixed

- Downgraded `PyJWT` requirement to `2.10.1` to resolve a fatal installation crash caused by an unsatisfiable dependency conflict with Home Assistant Core.

## [2.5.0] - 2026-04-08

### Minor Release

- Promoted all features and fixes from beta.
- Full details available in the GitHub Release notes.

## [2.3.0-beta.3627] - 2026-04-08

### Security

- Bumped `aiohttp` to 3.13.4 to resolve multiple GHSA vulnerabilities.
- Bumped `cryptography` to 46.0.7 to resolve GHSA-m959-cc7f-wv43 and GHSA-p423-j2cm-9vmq.
- Bumped `pillow` to 12.1.1.
- Bumped `PyJWT` to 2.12.0.
- Bumped `pyOpenSSL` to 26.0.0.
- Bumped `requests` to 2.33.0.
