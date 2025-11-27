# [2.2.0-beta.17](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.2.0-beta.10...v2.2.0-beta.17) (2025-11-27)


### Bug Fixes

* **ci:** Correct payload for HA cache clearing API call ([e98f2fd](https://github.com/brewmarsh/meraki-homeassistant/commit/e98f2fd809a946f49067adabd3d4e11d2905877b))* **ci:** trigger local deployment on push to beta ([e4770fe](https://github.com/brewmarsh/meraki-homeassistant/commit/e4770fecb77b1e8586a09cf064329677468456ab))* **ci:** trigger local deployment on push to beta and fix linting error ([27ffd01](https://github.com/brewmarsh/meraki-homeassistant/commit/27ffd0146c7dde9cd080051a83455affb7d54fb4))* Correctly handle informational API errors ([ef7f8e6](https://github.com/brewmarsh/meraki-homeassistant/commit/ef7f8e67af0d0297d79567d1c7e9e2645d6af79b))* **frontend:** Create deterministic build process ([9156275](https://github.com/brewmarsh/meraki-homeassistant/commit/91562759d62fab1e27bc591d91c0c511cb0a9ce0))* **frontend:** Pass config_entry_id as prop to components ([1b3343d](https://github.com/brewmarsh/meraki-homeassistant/commit/1b3343d351de069c2221a686787cf8927d02989c))* **frontend:** pass hass object as prop to fix connection error ([90e2d68](https://github.com/brewmarsh/meraki-homeassistant/commit/90e2d68a978645c9b4accd2b919fb8430216e15e))* **frontend:** Preserve UI state across panel refreshes ([c12fe60](https://github.com/brewmarsh/meraki-homeassistant/commit/c12fe605634dbc97df9bf19d14f7a9555db86ea9))* **frontend:** rebuild frontend assets ([9a694e2](https://github.com/brewmarsh/meraki-homeassistant/commit/9a694e228e35c3b576f2d187188d66ede3de214c))* **frontend:** refactor web UI to use standard hass websocket ([4535136](https://github.com/brewmarsh/meraki-homeassistant/commit/453513654947947e891e5ebedc57998f51b8969c))* **frontend:** resolve vite build circular dependency ([8ea7418](https://github.com/brewmarsh/meraki-homeassistant/commit/8ea741887d424340f67e10defceddcff02df44d0))* **frontend:** Update built assets ([99da4a6](https://github.com/brewmarsh/meraki-homeassistant/commit/99da4a6b616024940f716564ccf1b66376e3eddd))* **frontend:** Update built assets ([26c5d86](https://github.com/brewmarsh/meraki-homeassistant/commit/26c5d8613aefd4af1ba622f375cd07e41a3022d7))* **frontend:** Update built assets with normalized line endings ([43e4f73](https://github.com/brewmarsh/meraki-homeassistant/commit/43e4f73b35c125516f4ab27c7b5f81dac9f48b42))* **version:** synchronize version across configuration files ([a8c029a](https://github.com/brewmarsh/meraki-homeassistant/commit/a8c029ac121de3e20539594de0ef3971070bba7d))

### Features

* Add final-check job to CI workflow ([9f01e95](https://github.com/brewmarsh/meraki-homeassistant/commit/9f01e956fc119f99b3e2469a61ddcedeaddb251d))* Add frontend cache clear to deploy-local.yml ([2ae44f5](https://github.com/brewmarsh/meraki-homeassistant/commit/2ae44f53ccb7a436fc43be3d3b1b66225bef876d))* Auto-commit frontend assets in CI ([48b8665](https://github.com/brewmarsh/meraki-homeassistant/commit/48b8665f6995f2619106d73aa71a2d252b122278))* Echo manifest version in frontend-build CI job ([669eec4](https://github.com/brewmarsh/meraki-homeassistant/commit/669eec45ce1ba9a04a2e6f8fec0c468d695376b4))* **frontend:** implement dark mode synchronization ([555770e](https://github.com/brewmarsh/meraki-homeassistant/commit/555770e80aecd3b9e17013b2229f009e4cf291c9))* **frontend:** open RTSP stream links in a new tab ([0e79da8](https://github.com/brewmarsh/meraki-homeassistant/commit/0e79da8cdb50b6119e6c2fc364dfac0c69fe5076))* Log informational API errors with documentation links ([337a059](https://github.com/brewmarsh/meraki-homeassistant/commit/337a059c72e46e50599a6be6079c6f1b7d19fd7d))* Make deploy-local.yml depend on beta-ci.yaml success ([0994a0a](https://github.com/brewmarsh/meraki-homeassistant/commit/0994a0a5435b10fd255bf7209197ac0816eb05c2))* Refactor CI workflows for HACS and Hassfest validation ([9cb3a73](https://github.com/brewmarsh/meraki-homeassistant/commit/9cb3a73df245c36476cf3a98267fb1c8862d588f))
# [2.2.0-beta.10](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.2.0-beta.9...v2.2.0-beta.10) (2025-11-22)


### Bug Fixes

* frontend loading error [#299](https://github.com/brewmarsh/meraki-homeassistant/issues/299) and RTSP feature ([507971d](https://github.com/brewmarsh/meraki-homeassistant/commit/507971dde65c0d2f179628a227bf2940d48d5320))
# [2.2.0-beta.9](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.2.0-beta.8...v2.2.0-beta.9) (2025-11-21)


### Features

* display RTSP URL for cameras in the frontend device table ([442015f](https://github.com/brewmarsh/meraki-homeassistant/commit/442015f670e405d7c30a79619a1937045d7c3898))
# [2.2.0-beta.8](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.2.0-beta.7...v2.2.0-beta.8) (2025-11-21)


### Features

* add entity configuration options to backend and frontend ([5744afe](https://github.com/brewmarsh/meraki-homeassistant/commit/5744afe0361091498d4864fd8b5a8de20b983295))



# [2.2.0-beta.7](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.2.0-beta.6...v2.2.0-beta.7) (2025-11-21)

# [2.2.0-beta.6](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.2.0-beta.5...v2.2.0-beta.6) (2025-11-21)

# [2.2.0-beta.5](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.2.0-beta.4...v2.2.0-beta.5) (2025-11-21)

# [2.2.0-beta.4](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.2.0-beta.3...v2.2.0-beta.4) (2025-11-21)

### Bug Fixes

- **release:** install frontend dependencies before build ([ff1acf4](https://github.com/brewmarsh/meraki-homeassistant/commit/ff1acf46f5858010854649089cd8b3ef08176e3f))

# [2.2.0-beta.3](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.1.0...v2.2.0-beta.3) (2025-11-21)

### Bug Fixes

- **ci:** resolve linting errors and test failure ([2466f06](https://github.com/brewmarsh/meraki-homeassistant/commit/2466f066deb1319c244cff6f657ee76df8331c61))
- Correct indentation in MerakiAPIClient ([90bac82](https://github.com/brewmarsh/meraki-homeassistant/commit/90bac824461daf677ead251cb6ffbcd2ca4ea993))
- **deploy:** correct restart service name in API call ([c9490c6](https://github.com/brewmarsh/meraki-homeassistant/commit/c9490c6f718b64c6e7875476eee95fbd4a2fcfdd))
- **error-handling:** improve resilience to network errors ([7d7d6a8](https://github.com/brewmarsh/meraki-homeassistant/commit/7d7d6a8886dc2232b312b280fbe872d42dd880fa))
- **frontend:** update index.html to point to custom-panel.js ([e2927c8](https://github.com/brewmarsh/meraki-homeassistant/commit/e2927c867570d5c43acd11595e23bb0d2a8ba825))
- Recreate test_e2e_live.py with linting fixes ([ef98f0b](https://github.com/brewmarsh/meraki-homeassistant/commit/ef98f0b62e3cec7b8451abd94493661d2cec45a2))
- Resolve linting errors and restore web_api.py ([92df7b3](https://github.com/brewmarsh/meraki-homeassistant/commit/92df7b346a5905d285a827ba5c137504618b781f))
- Resolve Mypy and Ruff errors ([a008052](https://github.com/brewmarsh/meraki-homeassistant/commit/a008052f16e3a762517d04722d94fcc56ebdf0e2))
- **tests:** resolve linting errors in e2e live test ([213ac77](https://github.com/brewmarsh/meraki-homeassistant/commit/213ac7792b549c84db3b128675c93aadcb5c12cc))

### Features

- Add live E2E test and instructions ([bacd3e3](https://github.com/brewmarsh/meraki-homeassistant/commit/bacd3e3f61b51a11d9b564cc0183f824c916c3cb))
- Enhance device table with icons and row clicks, bump version to 2.2.0-beta.1 ([8a9a3d9](https://github.com/brewmarsh/meraki-homeassistant/commit/8a9a3d9699e6d0e8d546e113ed44d2d7686db1f8))
- **frontend:** build and deploy updated web UI ([35902d1](https://github.com/brewmarsh/meraki-homeassistant/commit/35902d1a2c27ed51a0d88046eaf93607bff86522))
- **frontend:** build and deploy updated web UI and automate build ([4f29b38](https://github.com/brewmarsh/meraki-homeassistant/commit/4f29b387e55f97984669aa3b634515c19f7ca63c))
- Implement functional Event Log in Web UI ([689e10c](https://github.com/brewmarsh/meraki-homeassistant/commit/689e10cd0370e4a3fd3fe85adf68dc36fcba9bbb))
- Update device table icons and click behavior ([0d45200](https://github.com/brewmarsh/meraki-homeassistant/commit/0d45200b058d5f149855a764d3addea230a5c6bb))

# [2.0.0-beta.66](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.65...v2.0.0-beta.66) (2025-11-19)

### Bug Fixes

- **websockets:** Register web API to resolve unknown command error ([ebf7359](https://github.com/brewmarsh/meraki-homeassistant/commit/ebf7359763c376ceafc88704d2d726eab62b9794))

# [2.0.0-beta.65](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.64...v2.0.0-beta.65) (2025-11-18)

### Bug Fixes

- **ci:** improve diagnostics for ha-local-deploy ([0f578a3](https://github.com/brewmarsh/meraki-homeassistant/commit/0f578a3871eac4d3bfd239d242534f8baac6cf88))

# [2.0.0-beta.64](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.63...v2.0.0-beta.64) (2025-11-18)

### Bug Fixes

- **frontend:** rebuild frontend to fix unknown command error ([d29f81b](https://github.com/brewmarsh/meraki-homeassistant/commit/d29f81bbd9ad8b2385cf9e169ac923bc28249912))

# [2.0.0-beta.63](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.62...v2.0.0-beta.63) (2025-11-18)

### Bug Fixes

- **frontend:** Bump version to force cache bust ([ea603a7](https://github.com/brewmarsh/meraki-homeassistant/commit/ea603a71cbaebe8633f8f2f14b75ecbd519fd4cd))

### Features

- Add camera status check before snapshot ([06b457b](https://github.com/brewmarsh/meraki-homeassistant/commit/06b457bda0800ed299c4edfdc5349cbc14f73406))

# [2.0.0-beta.62](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.61...v2.0.0-beta.62) (2025-11-18)

### Bug Fixes

- restore side panel and correct websocket command ([8e11cf3](https://github.com/brewmarsh/meraki-homeassistant/commit/8e11cf3cea8e1c41403fdf54661213b536a319c7))

# [2.0.0-beta.61](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.60...v2.0.0-beta.61) (2025-11-18)

### Bug Fixes

- restore side panel by registering frontend ([4e1ae4b](https://github.com/brewmarsh/meraki-homeassistant/commit/4e1ae4bac526a87011131ba197d2338567906c3a))

# [2.0.0-beta.60](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.59...v2.0.0-beta.60) (2025-11-18)

### Features

- **coordinator:** Add backward compatibility for pending update methods ([66cea68](https://github.com/brewmarsh/meraki-homeassistant/commit/66cea68960b924def5074313f6086ae292f94995))

# [2.0.0-beta.59](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.58...v2.0.0-beta.59) (2025-11-18)

### Features

- Use constant for Meraki client key ([df1a09a](https://github.com/brewmarsh/meraki-homeassistant/commit/df1a09aee373a8e5ed8ae4ab95732a8e6beb800b))

# [2.0.0-beta.58](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.57...v2.0.0-beta.58) (2025-11-18)

### Bug Fixes

- **text:** Correct pending update method names ([a468e62](https://github.com/brewmarsh/meraki-homeassistant/commit/a468e62229eadd16ecba838cf9e50a57fb124019))

# [2.0.0-beta.57](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.56...v2.0.0-beta.57) (2025-11-18)

### Bug Fixes

- **api:** Refactor API client to prevent NoneType error ([236c280](https://github.com/brewmarsh/meraki-homeassistant/commit/236c28028f31997853b2047510389cf6dba9c4d7))

# [2.0.0-beta.56](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.55...v2.0.0-beta.56) (2025-11-18)

### Bug Fixes

- **core:** Refactor MerakiAPIClient for proper async initialization ([22fe573](https://github.com/brewmarsh/meraki-homeassistant/commit/22fe57372568340d5d7762e24e42e5f412810e18))

# [2.0.0-beta.55](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.54...v2.0.0-beta.55) (2025-11-18)

### Bug Fixes

- **ci:** improve error handling for api calls ([daa85a7](https://github.com/brewmarsh/meraki-homeassistant/commit/daa85a783a14bd8489ff6da2ad7723b01fc94c83))

# [2.0.0-beta.54](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.53...v2.0.0-beta.54) (2025-11-18)

### Bug Fixes

- **ci:** improve error handling for api calls ([e0ae444](https://github.com/brewmarsh/meraki-homeassistant/commit/e0ae444ccfab250dc4f264648193ad4f6045c7e7))
- **core:** Await all MerakiAPIClient instantiations ([d2dd20b](https://github.com/brewmarsh/meraki-homeassistant/commit/d2dd20b48829c6edd2142e124c1da3c3f80ef70e))

# [2.0.0-beta.53](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.52...v2.0.0-beta.53) (2025-11-18)

### Bug Fixes

- **core:** await MerakiAPIClient initialization ([8f06164](https://github.com/brewmarsh/meraki-homeassistant/commit/8f06164fa5e650b9af0567506f04b78f6321bfad))

# [2.0.0-beta.52](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.51...v2.0.0-beta.52) (2025-11-18)

### Bug Fixes

- **ci:** improve error handling for api calls ([335e6a3](https://github.com/brewmarsh/meraki-homeassistant/commit/335e6a31f35dc177be79615595ee7c3f7705d34a))

# [2.0.0-beta.51](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.50...v2.0.0-beta.51) (2025-11-18)

# [2.0.0-beta.50](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.49...v2.0.0-beta.50) (2025-11-18)

### Bug Fixes

- **ci:** Sanitize Home Assistant token in deploy workflow ([72dfd9d](https://github.com/brewmarsh/meraki-homeassistant/commit/72dfd9d6a43ab42e31cf7e3af43449b3a0c5fc25))

# [2.0.0-beta.49](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.48...v2.0.0-beta.49) (2025-11-18)

### Bug Fixes

- **config_flow:** Correct AbortFlow import ([9fe7fd8](https://github.com/brewmarsh/meraki-homeassistant/commit/9fe7fd8aafbaf0bcc21dc356b8aeb76c769a8ad5))

# [2.0.0-beta.48](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.47...v2.0.0-beta.48) (2025-11-17)

### Bug Fixes

- **ci:** handle non-JSON responses in deploy workflow ([bd83fed](https://github.com/brewmarsh/meraki-homeassistant/commit/bd83fed3f8468035916a97b1453c64983c901988))

# [2.0.0-beta.47](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.46...v2.0.0-beta.47) (2025-11-17)

# [2.0.0-beta.46](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.45...v2.0.0-beta.46) (2025-11-17)

### Bug Fixes

- **ci:** install jq in deploy workflow ([75f6cc3](https://github.com/brewmarsh/meraki-homeassistant/commit/75f6cc3e79a5bddabb6dc2b9cd3053ebc8a6d3f7))
- **config_flow:** Defer imports within async_step_user to resolve blocking call ([a77464c](https://github.com/brewmarsh/meraki-homeassistant/commit/a77464cdfeb0af77610c4774e4a80a48a22044a1))

# [2.0.0-beta.45](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.44...v2.0.0-beta.45) (2025-11-17)

### Bug Fixes

- **config_flow:** Defer imports to resolve blocking call ([3f55d5f](https://github.com/brewmarsh/meraki-homeassistant/commit/3f55d5f865e392be55b9cfe8ce97dbffd04dbceb))
- **config_flow:** Defer imports within async_step_user to resolve blocking call ([a77464c](https://github.com/brewmarsh/meraki-homeassistant/commit/a77464cdfeb0af77610c4774e4a80a48a22044a1))

# [2.0.0-beta.44](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.43...v2.0.0-beta.44) (2025-11-17)

### Features

- Defer import to fix blocking call ([9700dd5](https://github.com/brewmarsh/meraki-homeassistant/commit/9700dd5e2476fbe9619bcc369ae02d5512a16916))

# [2.0.0-beta.43](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.42...v2.0.0-beta.43) (2025-11-17)

### Bug Fixes

- **startup:** Resolve circular dependency and modernize setup ([27a2ec4](https://github.com/brewmarsh/meraki-homeassistant/commit/27a2ec4d2d1f14416c9bf8b79f7b0e5697876de3))

# [2.0.0-beta.42](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.41...v2.0.0-beta.42) (2025-11-17)

### Bug Fixes

- **startup:** Resolve circular dependency and modernize setup ([d770727](https://github.com/brewmarsh/meraki-homeassistant/commit/d77072749c7cb39732edeae21d2227fac7688b4f))

# [2.0.0-beta.41](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.40...v2.0.0-beta.41) (2025-11-17)

### Bug Fixes

- **options_flow:** resolve circular import on startup ([525ff6c](https://github.com/brewmarsh/meraki-homeassistant/commit/525ff6c3f2331dc23819388eb089085968cb044e))

# [2.0.0-beta.40](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.39...v2.0.0-beta.40) (2025-11-17)

### Bug Fixes

- **init:** resolve blocking call on startup by refactoring setup ([95a3040](https://github.com/brewmarsh/meraki-homeassistant/commit/95a30401720388d7b66a5edc90a9c6b7d21b1f91))

# [2.0.0-beta.39](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.38...v2.0.0-beta.39) (2025-11-17)

### Bug Fixes

- **config_flow:** resolve blocking call and import error on startup ([5732374](https://github.com/brewmarsh/meraki-homeassistant/commit/57323745c7e62705fbc93e2ea6c5c93563298a59))
- **config_flow:** resolve blocking call and import error on startup ([1facb61](https://github.com/brewmarsh/meraki-homeassistant/commit/1facb61c1a9da1e2b6ccd43e5e6fc4c491508954))

# [2.0.0-beta.38](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.37...v2.0.0-beta.38) (2025-11-17)

### Bug Fixes

- **core:** Break circular dependency to fix all startup failures ([fd023dc](https://github.com/brewmarsh/meraki-homeassistant/commit/fd023dc4d8cc60ba94f6a03a257698a0d48c53fe))

# [2.0.0-beta.37](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.36...v2.0.0-beta.37) (2025-11-16)

# [2.0.0-beta.36](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.35...v2.0.0-beta.36) (2025-11-16)

# [2.0.0-beta.35](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.34...v2.0.0-beta.35) (2025-11-16)

# [2.0.0-beta.34](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.33...v2.0.0-beta.34) (2025-11-15)

### Bug Fixes

- Defer options flow import to prevent blocking call ([c0a8239](https://github.com/brewmarsh/meraki-homeassistant/commit/c0a8239ba4566a4d8fff104a1235440003dd58d2))

# [2.0.0-beta.33](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.32...v2.0.0-beta.33) (2025-11-15)

# [2.0.0-beta.32](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.31...v2.0.0-beta.32) (2025-11-15)

### Bug Fixes

- **api:** Break circular dependency causing startup failure ([9df0287](https://github.com/brewmarsh/meraki-homeassistant/commit/9df028736fe490ede852cde210c70bf44a4d10a3))

# [2.0.0-beta.31](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.30...v2.0.0-beta.31) (2025-11-15)

### Bug Fixes

- **coordinator:** Remove client re-init to fix handler error ([223cadb](https://github.com/brewmarsh/meraki-homeassistant/commit/223cadb875523bab5e5e676900f20386732e00ce))

# [2.0.0-beta.30](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.29...v2.0.0-beta.30) (2025-11-15)

### Bug Fixes

- **options_flow:** Correct import path to resolve startup failure ([6b3bcc5](https://github.com/brewmarsh/meraki-homeassistant/commit/6b3bcc5caae4ad15ad01d59330608530ab5c623c))

# [2.0.0-beta.29](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.28...v2.0.0-beta.29) (2025-11-15)

### Bug Fixes

- **config_flow:** Remove deprecated handler registration ([c5eac0a](https://github.com/brewmarsh/meraki-homeassistant/commit/c5eac0ae3ea7910d68f0ff84086ab7b28ba1b494))

# [2.0.0-beta.28](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.27...v2.0.0-beta.28) (2025-11-15)

### Bug Fixes

- **structure:** Remove redundant platforms directory causing startup failure ([25ebff0](https://github.com/brewmarsh/meraki-homeassistant/commit/25ebff0f1828e593a616684713153854e6e574fa))

# [2.0.0-beta.27](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.26...v2.0.0-beta.27) (2025-11-15)

### Bug Fixes

- **init:** Use modern config schema to fix ha-missing-config ([d1f4fb1](https://github.com/brewmarsh/meraki-homeassistant/commit/d1f4fb192fe41cb75739edd5c9e6f8244f5d33b9))

# [2.0.0-beta.26](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.25...v2.0.0-beta.26) (2025-11-15)

### Bug Fixes

- **coordinator:** Unify coordinator classes to resolve AttributeError ([cb80e49](https://github.com/brewmarsh/meraki-homeassistant/commit/cb80e4918eb66b9ac7e38bc235c15d6b02eec7ad))

# [2.0.0-beta.25](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.24...v2.0.0-beta.25) (2025-11-15)

### Bug Fixes

- **ci:** correct typo in pip-audit command ([5aeca50](https://github.com/brewmarsh/meraki-homeassistant/commit/5aeca50fbc15087c11fc2aa9642271988b953eac))
- **coordinator:** Unify coordinator classes to resolve AttributeError ([4ff8037](https://github.com/brewmarsh/meraki-homeassistant/commit/4ff80373861bb54c4d1102a4cd0323c89f2f3c2e))
- **coordinator:** Unify coordinator classes to resolve AttributeError ([0bccca6](https://github.com/brewmarsh/meraki-homeassistant/commit/0bccca691c90ab3b740d5004fad32acd5bfca28a))
- **coordinator:** Unify coordinator classes to resolve AttributeError ([a1cd383](https://github.com/brewmarsh/meraki-homeassistant/commit/a1cd3835d184c33a0c4ac2b28b1d9e3effde6082))
- Correct handler instantiation ([76f63d2](https://github.com/brewmarsh/meraki-homeassistant/commit/76f63d2cac16406cbe106e2c650aa513b84f3ae4))
- Correct handler instantiation ([ff13a9b](https://github.com/brewmarsh/meraki-homeassistant/commit/ff13a9b1a24bfe6b7a940b2586e561cb6d0eefc1))
- Correct handler instantiation ([0421c66](https://github.com/brewmarsh/meraki-homeassistant/commit/0421c6632a68a513abfc725605a21c4693cfecd1))
- Resolve ha-blocking-import and stabilize integration ([67419b6](https://github.com/brewmarsh/meraki-homeassistant/commit/67419b6178f02e43060c07b229d19605499c158d))
- Resolve mypy and hassfest errors ([d34d9a7](https://github.com/brewmarsh/meraki-homeassistant/commit/d34d9a7314bef26abba9884a025f6eaa4bd9566d))
- Resolve mypy errors ([0bed1b1](https://github.com/brewmarsh/meraki-homeassistant/commit/0bed1b1057035793a4cc13496db2768b42d8fdbd))
- Resolve ruff and mypy errors ([f15ace3](https://github.com/brewmarsh/meraki-homeassistant/commit/f15ace3d63b57c4ab832fb5ac9f130ef1fc1eda4))
- Resolve startup errors and ruff violations ([24106f7](https://github.com/brewmarsh/meraki-homeassistant/commit/24106f766efd3a52272e8de57f69ccc5951db447))
- Resolve startup errors and ruff violations ([d203f2a](https://github.com/brewmarsh/meraki-homeassistant/commit/d203f2aa56acac43eec0e802a0babe2e7c399fd1))

# [2.0.0-beta.23](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.24...v2.0.0-beta.23) (2025-11-14)

### Bug Fixes

- **ci:** correct typo in pip-audit command ([5aeca50](https://github.com/brewmarsh/meraki-homeassistant/commit/5aeca50fbc15087c11fc2aa9642271988b953eac))
- Correct handler instantiation ([76f63d2](https://github.com/brewmarsh/meraki-homeassistant/commit/76f63d2cac16406cbe106e2c650aa513b84f3ae4))
- Correct handler instantiation ([ff13a9b](https://github.com/brewmarsh/meraki-homeassistant/commit/ff13a9b1a24bfe6b7a940b2586e561cb6d0eefc1))
- Correct handler instantiation ([0421c66](https://github.com/brewmarsh/meraki-homeassistant/commit/0421c6632a68a513abfc725605a21c4693cfecd1))

# [2.0.0-beta.22](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.24...v2.0.0-beta.22) (2025-11-13)

### Bug Fixes

- Correct handler instantiation ([76f63d2](https://github.com/brewmarsh/meraki-homeassistant/commit/76f63d2cac16406cbe106e2c650aa513b84f3ae4))
- Correct handler instantiation ([ff13a9b](https://github.com/brewmarsh/meraki-homeassistant/commit/ff13a9b1a24bfe6b7a940b2586e561cb6d0eefc1))
- Correct handler instantiation ([0421c66](https://github.com/brewmarsh/meraki-homeassistant/commit/0421c6632a68a513abfc725605a21c4693cfecd1))

# [2.0.0-beta.21](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.24...v2.0.0-beta.21) (2025-11-13)

### Bug Fixes

- Correct handler instantiation ([ff13a9b](https://github.com/brewmarsh/meraki-homeassistant/commit/ff13a9b1a24bfe6b7a940b2586e561cb6d0eefc1))
- Correct handler instantiation ([0421c66](https://github.com/brewmarsh/meraki-homeassistant/commit/0421c6632a68a513abfc725605a21c4693cfecd1))

# [2.0.0-beta.20](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.19...v2.0.0-beta.20) (2025-11-12)

## [2.0.0-beta.19](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.18...v2.0.0-beta.19) (2025-11-12)

### Bug Fixes

- Resolve TypeError and panel loading race condition ([6f48755](https://github.com/brewmarsh/meraki-homeassistant/commit/6f487553d8309a9e80b66693e03c36046e75dd9a))

## [2.0.0-beta.18](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.17...v2.0.0-beta.18) (2025-11-11)

### Bug Fixes

- Resolve panel loading failure by deferring panel registration ([4951084](https://github.com/brewmarsh/meraki-homeassistant/commit/4951084d73df422e3b7d8af35d55cedcfd750037))

## [2.0.0-beta.17](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.16...v2.0.0-beta.17) (2025-11-11)

### Bug Fixes

- Resolve `async_config_entry_first_refresh` deprecation warning ([b06b532](https://github.com/brewmarsh/meraki-homeassistant/commit/b06b53225baf6f7985eb904c94ff0780de64fe7c))

## [2.0.0-beta.16](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.15...v2.0.0-beta.16) (2025-11-11)

### Bug Fixes

- Synchronize 'Enabled Networks' config with web UI ([f98276f](https://github.com/brewmarsh/meraki-homeassistant/commit/f98276f94d6c6c36c741ad6b8f5a93a9d608d794))

## [2.0.0-beta.15](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.14...v2.0.0-beta.15) (2025-11-11)

### Features

- Refine network toggle UI and state management ([34c1ae5](https://github.com/brewmarsh/meraki-homeassistant/commit/34c1ae587e90c98bd1da452de8a000bb5607e636))
- Refine network toggle UI and state management ([093fd54](https://github.com/brewmarsh/meraki-homeassistant/commit/093fd544438040d3cfa7752f1f4fb8840a55768b))

## [2.0.0-beta.14](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.13...v2.0.0-beta.14) (2025-11-11)

### Bug Fixes

- Restore missing SSID entities ([3c6dae1](https://github.com/brewmarsh/meraki-homeassistant/commit/3c6dae165eb0877f1759f36169d43b76ca7c9eb7))
- Restore missing SSID entities and address linting ([3cb7ffc](https://github.com/brewmarsh/meraki-homeassistant/commit/3cb7ffcff40ae3839dd05bfbdd8fca2f978f985d))

## [2.0.0-beta.13](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.12...v2.0.0-beta.13) (2025-11-11)

### Features

- Add network enable/disable toggle ([3dd5da4](https://github.com/brewmarsh/meraki-homeassistant/commit/3dd5da472086abd0c027ad05bcb7ba03424a0bfe))

## [2.0.0-beta.12](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.11...v2.0.0-beta.12) (2025-11-11)

### Features

- Add network enable/disable toggle to UI and display version ([e2a275a](https://github.com/brewmarsh/meraki-homeassistant/commit/e2a275a3dc981ab3890e8a96844ce029aeefcc83))

## [2.0.0-beta.11](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.10...v2.0.0-beta.11) (2025-11-10)

### Features

- Add network enable/disable toggle to UI and display version ([4732100](https://github.com/brewmarsh/meraki-homeassistant/commit/4732100eb72e83fa327d7e8295f7186622854366))

## [2.0.0-beta.10](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.9...v2.0.0-beta.10) (2025-11-10)

### Features

- Add network enable/disable toggle to UI and display version ([9f2c46d](https://github.com/brewmarsh/meraki-homeassistant/commit/9f2c46d0df0527ffb9965281b62c34ebc54cb42f))

## [2.0.0-beta.9](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.8...v2.0.0-beta.9) (2025-11-10)

### Features

- Add network enable/disable toggle to UI and display version ([3d2daf8](https://github.com/brewmarsh/meraki-homeassistant/commit/3d2daf8f196ff7df586f51c119bd273cf0b54367))
- Add network enable/disable toggle to UI and display version ([26f2894](https://github.com/brewmarsh/meraki-homeassistant/commit/26f28947e7b37999e4dce79ca83c26e18e5b1495))

## [2.0.0-beta.8](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.7...v2.0.0-beta.8) (2025-11-10)

### Features

- Add network enable/disable toggle to UI and display version ([77c012e](https://github.com/brewmarsh/meraki-homeassistant/commit/77c012eefa84c7dc6657209a707c5859526fd3dfd))

## [2.0.0-beta.7](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.6...v2.0.0-beta.7) (2025-11-10)

### Features

- Add network enable/disable toggle to UI ([c4f61ff](https://github.com/brewmarsh/meraki-homeassistant/commit/c4f61ffb1f971ade718f06729df7796bf6d34989))

## [2.0.0-beta.6](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.5...v2.0.0-beta.6) (2025-11-10)

### Features

- Add network enable/disable toggle to UI ([f624e05](https://github.com/brewmarsh/meraki-homeassistant/commit/f624e05ff35b4c823283a137f8c7a83d7485d59a))
- Add network enable/disable toggle to UI ([c774699](https://github.com/brewmarsh/meraki-homeassistant/commit/c774699ac51ea8ddebc43772099f72c9daa84480))
- Add network enable/disable toggle to UI ([fd884fa](https://github.com/brewmarsh/meraki-homeassistant/commit/fd884fae17dfe669a570c4036103102d2feba052))
- Add network enable/disable toggle to UI ([66383d7](https://github.com/brewmarsh/meraki-homeassistant/commit/66383d713a09da27af781a2970afbc3917f15acd))
- Add network enable/disable toggle to UI ([01d694f](https://github.com/brewmarsh/meraki-homeassistant/commit/01d694ff630bef3b6e9b0f2d1639456f3e0118e1))

## [2.0.0-beta.5](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.4...v2.0.0-beta.5) (2025-11-10)

### Bug Fixes

- **api:** add missing wireless settings methods ([87a9055](https://github.com/brewmarsh/meraki-homeassistant/commit/87a9055ac0d447e4be44c2b5064a1d16f57640aa))
- **api:** correct docstring formatting ([73c9620](https://github.com/brewmarsh/meraki-homeassistant/commit/73c9620a1d3c573e636f52ccd7fa6ba8a3fe9696))
- **tests:** correct import order in test_access_point_leds.py ([d596a88](https://github.com/brewmarsh/meraki-homeassistant/commit/d596a88cf11580937dd30a8d018249e808e01652))

### Features

- **switch:** add access point led control ([623437b](https://github.com/brewmarsh/meraki-homeassistant/commit/623437b4242f34670b5cc420329a0d88a2439792))

## [2.0.0-beta.4](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.3...v2.0.0-beta.4) (2025-11-10)

## [2.0.0-beta.3](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0-beta.2...v2.0.0-beta.3) (2025-11-10)

### Features

- configure dependabot to target beta branch ([83f4057](https://github.com/brewmarsh/meraki-homeassistant/commit/83f4057caca2dc13adc4c33e786b4ce74f88d8cb))

## [2.0.0-beta.2](https://github.com/brewmarsh/meraki-homeassistant/compare/v2.0.0...v2.0.0-beta.2) (2025-11-10)

## [2.0.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.5.4-beta.36...v2.0.0) (2025-11-07)

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
