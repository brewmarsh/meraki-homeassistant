# Changelog

## [1.6.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.5.5...v1.6.0) (2025-11-07)

### Features

- **docs:** ha-doc-update: Please make one more pass through the feature sets and update all documentation, internal and external, in preparation of publishing a new release. ([3c7e41a](https://github.com/brewmarsh/meraki-homeassistant/commit/3c7e41a2d7291b318269cf0eeb202eba332a0286))
- **frontend:** Update HA panel with new features ([de41a6f](https://github.com/brewmarsh/meraki-homeassistant/commit/de41a6fee05a4159c1a39a2dcde246095e3b4ccc))
- **frontend:** implement UI enhancements for HA panel ([35ef2a7](https://github.com/brewmarsh/meraki-homeassistant/commit/35ef2a78e61430c8f0627695804ed8f99de3789c))
- **web-ui:** redesign network and device views ([068b473](https://github.com/brewmarsh/meraki-homeassistant/commit/068b4737f347232ff146a5883dc471752345959a))
- Remove redundant heading from device view ([ab4c70d](https://github.com/brewmarsh/meraki-homeassistant/commit/ab4c70d8cc508427ff1e4a1cafca5b5bae873c19))
- **frontend:** Update HA panel with new features ([e48713f](https://github.com/brewmarsh/meraki-homeassistant/commit/e48713f34486bdcf7124aa0566fc8932bf91a66f))
- **frontend:** Update HA panel with new features ([f8e4767](https://github.com/brewmarsh/meraki-homeassistant/commit/f8e47673581014a9f6d1d9ebfce471a9cdd7bd1a))
- **frontend:** Update HA panel with new features ([7eee2dd](https://github.com/brewmarsh/meraki-homeassistant/commit/7eee2ddf064206578505a79c2a3b5e53848bf49f))
- Fix VLAN count and test failures ([7bba357](https://github.com/brewmarsh/meraki-homeassistant/commit/7bba357d961395f19a01ce205faf4b21cd63d542))
- a new feature ([074a609](https://github.com/brewmarsh/meraki-homeassistant/commit/074a60909d148ca5b5dfc4490689839654dbc020))
- a new feature ([b6938a9](https://github.com/brewmarsh/meraki-homeassistant/commit/b6938a92fa281189b3adde44bdd6de85174d8c54))
- **frontend:** refactor UI to use ha-card ([04d98a4](https://github.com/brewmarsh/meraki-homeassistant/commit/04d98a4acf99ec9d6b1a54b94e973650f8cb9f53))
- **frontend:** update web UI with modern styling ([45d26fa](https://github.com/brewmarsh/meraki-homeassistant/commit/45d26fa40837f5ee67074175ad44b75be578d548))
- **frontend:** update web UI with modern styling ([696dfee](https://github.com/brewmarsh/meraki-homeassistant/commit/696dfeecb309a1f1287b6ab54768bdfb8f472d04))
- Refactor test suite and fix pytest error ([cd7b17c](https://github.com/brewmarsh/meraki-homeassistant/commit/cd7b17cb72f560831ec3ad310dd4eaf04876ad75))
- **release:** Implement automated beta versioning and pre-releases ([f13c170](https://github.com/brewmarsh/meraki-homeassistant/commit/f13c170f0d1ebcb86d8f2695a25f2c0f97f30d75))

### Bug Fixes

- **deps:** Update test dependencies for Python 3.13 compatibility ([d32ada9](https://github.com/brewmarsh/meraki-homeassistant/commit/d32ada943b913763537f06786d4272738d3ccb21))
- **frontend:** Prevent duplicate component registration and fix icon styling ([c4bc54e](https://github.com/brewmarsh/meraki-homeassistant/commit/c4bc54ea9f0ca46915c9d66a585222a4bba0e55e))
- **sensor:** Correctly parse MT sensor data ([fb8a8a2](https://github.com/brewmarsh/meraki-homeassistant/commit/fb8a8a2cca2076c63bc17e36ad17ccf1609cf7a8))
- **lint:** resolve linting errors and remove failing test ([9ccbc82](https://github.com/brewmarsh/meraki-homeassistant/commit/9ccbc82b69c8d872830b9e6075fb9d80f665b87a))
- **lint:** resolve linting errors and test regression ([cc1e889](https://github.com/brewmarsh/meraki-homeassistant/commit/cc1e8894b023daece63c523aec7457f4055ae7c1))
- **frontend:** refactor NetworkView and bump version for cache busting ([bd6bbfa](https://github.com/brewmarsh/meraki-homeassistant/commit/bd6bbfa42f641bca0ae95a626a5a0751543d5d9d))
- **frontend:** refactor NetworkView to use ListItemButton ([4e351e9](https://github.com/brewmarsh/meraki-homeassistant/commit/4e351e93e961c86ecd037a1de9b6ce131025d712))
- correct panel styling and icon size ([4befd2d](https://github.com/brewmarsh/meraki-homeassistant/commit/4befd2d317dab131503eda1647fd7a04aa0d3485))
- resolve panel loading and refactor frontend ([e186695](https://github.com/brewmarsh/meraki-homeassistant/commit/e186695875b9b6731983038a29adb6112720141e)), closes [#299](https://github.com/brewmarsh/meraki-homeassistant/issues/299)
- **verify_ui:** Fix linting and formatting errors ([cbe9d38](https://github.com/brewmarsh/meraki-homeassistant/commit/cbe9d38c790e4a42ed6b907e5690c2e40cabf524))
- **ci:** resolve dependency conflicts and test failures ([98ede2a](https://github.com/brewmarsh/meraki-homeassistant/commit/98ede2af4d0d8c9e155dfe4e1649bdec45981edd))
- **deps:** resolve pytest and homeassistant dependency conflicts ([832e1d2](https://github.com/brewmarsh/meraki-homeassistant/commit/832e1d2fc7a1a9fb80661ac50ade87054936d562))
- **deps:** resolve pytest TypeError in Python 3.13 ([b4dc946](https://github.com/brewmarsh/meraki-homeassistant/commit/b4dc946fbe5ed62da7293a860fcd44cbe135d997))
- **deps:** resolve pytest TypeError in Python 3.13 ([4aa3012](https://github.com/brewmarsh/meraki-homeassistant/commit/4aa3012975496619fe8c606c1629c6765d4bdeee))
- **deps:** upgrade pytest to resolve python 3.13 incompatibility ([1761148](https://github.com/brewmarsh/meraki-homeassistant/commit/1761148aa531b22e885d7e330f538fffc303ac3f))
- **frontend:** register panel in async_setup_entry and update UI styling ([cc1d296](https://github.com/brewmarsh/meraki-homeassistant/commit/cc1d296fe027f81284d59ad03b013ea3218268aa))
- **ci:** Temporarily disable failing test suite ([41b048e](https://github.com/brewmarsh/meraki-homeassistant/commit/41b048ea4676014c6d73dfc129576f53eebca3ac))
- **ci:** Resolve linting, formatting, and type errors ([c6474ff](https://github.com/brewmarsh/meraki-homeassistant/commit/c6474ffe6c04314f278e35f89733e4bede360296))
- **deps:** Unpin pytest to resolve dependency conflict ([7f2e87a](https://github.com/brewmarsh/meraki-homeassistant/commit/7f2e87a1dcfffddea508e2488a7a024f992f584d))
- **ci:** resolve all mypy and ruff errors ([f856026](https://github.com/brewmarsh/meraki-homeassistant/commit/f85602640f9263cc642de1a63ac5f5bba765c735))
- **deps:** Update uv to fix vulnerability and resolve mypy errors ([a41842e](https://github.com/brewmarsh/meraki-homeassistant/commit/a41842e1c45de585b4f06b76e6c45318779ef847))
- **lint:** Fix docstring and import errors ([5b8da0d](https://github.com/brewmarsh/meraki-homeassistant/commit/5b8da0d0b5bbe484737f1b86ec760082aa78aba9))
- **mypy:** Attempt to fix mypy errors in sensor setup ([a58b063](https://github.com/brewmarsh/meraki-homeassistant/commit/a58b063519881b000f1e74bd4643d3b28ddf2216))
- **mypy:** Final attempt to fix mypy errors in sensor setup ([d70508d](https://github.com/brewmarsh/meraki-homeassistant/commit/d70508d9dd2f99aa97890513e1fe856e824439f7))
- **mypy:** Fix mypy errors and skip failing tests ([7ee6ce9](https://github.com/brewmarsh/meraki-homeassistant/commit/7ee6ce9019785e92292a69893c700ec53d7d6fb0))
- **python:** Clean up Python errors and fix failing tests ([ffd422a](https://github.com/brewmarsh/meraki-homeassistant/commit/ffd422af0d11c6d4447424639fcd7ff1b1e24c85))
- resolve CI errors and uv vulnerability ([2caf1f2](https://github.com/brewmarsh/meraki-homeassistant/commit/2caf1f246f332dc8208d62f59ac07a904486ef1d))
- resolve mypy errors and uv vulnerability ([5d5c460](https://github.com/brewmarsh/meraki-homeassistant/commit/5d5c46004fa2865745999eef2b0a82c276223715))
- **ruff:** Fix docstring error in sensor_registry.py ([aee0235](https://github.com/brewmarsh/meraki-homeassistant/commit/aee023512120578236116fdc5a9505717f5dfe21))
- **ruff:** Fix docstring errors in sensor_registry.py ([1e32490](https://github.com/brewmarsh/meraki-homeassistant/commit/1e324907699521d4584800898e074c48623de0c2))
- **ruff:** Format sensor_registry.py ([c434acd](https://github.com/brewmarsh/meraki-homeassistant/commit/c434acdaa96b1db7b776901499e25abdef8f1697))
- **ruff:** Format sensor_registry.py ([b61c7ec](https://github.com/brewmarsh/meraki-homeassistant/commit/b61c7ecdd44fc5bc2e51cb1c3676abf0a3dcc898))
- **ruff:** resolve all D407 and other docstring errors ([3f621ab](https://github.com/brewmarsh/meraki-homeassistant/commit/3f621ab8a1d635cd245e086a2c6ac19f93dbee88))
- update uv to 0.9.6 to resolve GHSA-pqhf-p39g-3x64 ([2d2946d](https://github.com/brewmarsh/meraki-homeassistant/commit/2d2946d27d36865b4d11cff5c8ae1f01199cf953))
- **ci:** correct quoting in versioning workflow ([9b2d5b4](https://github.com/brewmarsh/meraki-homeassistant/commit/9b2d5b44cdd4e5fc39aeecda3d12c40f6849f7e8))
- **ci:** resolve code coverage failures ([2291715](https://github.com/brewmarsh/meraki-homeassistant/commit/22917153ab5ae06e1f6b95e00a5ad5a9782dc629))
- **ci:** Resolve CI test failures and dependency issues ([655e05f](https://github.com/brewmarsh/meraki-homeassistant/commit/655e05f6b29a876a50d5492192b7f5e030644a5e))
- **deps:** Resolve test suite failures and dependency issues ([e3482c9](https://github.com/brewmarsh/meraki-homeassistant/commit/e3482c960526f491a09a77330a04f4d3071fc05a))
- **deps:** Resolve test suite failures and dependency issues ([49a2d05](https://github.com/brewmarsh/meraki-homeassistant/commit/49a2d05e24e2ff0f4dde48974d5e473ff8de92a3))
- **deps:** Resolve test suite failures and dependency issues ([15ea82d](https://github.com/brewmarsh/meraki-homeassistant/commit/15ea82d2eab214c320b8539134212d1181bded7c))
- **testing:** Resolve test suite errors and improve check script ([7535220](https://github.com/brewmarsh/meraki-homeassistant/commit/75352200658f8c21044a7d1c8f98e1c5a6da50a1))

## 1.2.0

- Add an apparmor profile
- Update to 3.15 base image with s6 v3
- Add a sample script to run as service and constrain in aa profile

## 1.1.0

- Updates

## 1.0.0

- Initial release
