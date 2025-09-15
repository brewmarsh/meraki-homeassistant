## [1.5.1](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.5.0...v1.5.1) (2025-09-15)



# [1.5.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.4.2...v1.5.0) (2025-08-25)


### Bug Fixes

* **api:** Add missing endpoint wrappers for coordinators ([4124e29](https://github.com/brewmarsh/meraki-homeassistant/commit/4124e29eed2b3fe8a83d6054027369814c14dd9a))
* **api:** Correct method names for L7 firewall rules ([28821a0](https://github.com/brewmarsh/meraki-homeassistant/commit/28821a0bfaf75087f509c0b2cbb4442a2131d3ee))
* **api:** Use correct object for L7 firewall rule calls ([58ebd2c](https://github.com/brewmarsh/meraki-homeassistant/commit/58ebd2cfcd3554df499edc5ddb420a5458eda4a7))
* Consolidate parental controls backend and UI fixes ([0049dca](https://github.com/brewmarsh/meraki-homeassistant/commit/0049dca0932d858b3de71eb5625de77e20bce2a4))
* **coordinator:** Add get_network and get_ssid helpers ([086e7d4](https://github.com/brewmarsh/meraki-homeassistant/commit/086e7d483e7844bc3fc3f96adacdd9c5fc79bb3c))
* **coordinator:** Add resilience to partial API failures ([640b660](https://github.com/brewmarsh/meraki-homeassistant/commit/640b660613a08768c892d3de8371a8502170665c))
* **coordinator:** Correct relative import path ([a07d9b7](https://github.com/brewmarsh/meraki-homeassistant/commit/a07d9b7b88bab0e94455086646218ab9e39c1226))
* **coordinator:** Recreate ClientFirewallCoordinator and add graceful failure ([8bf11a1](https://github.com/brewmarsh/meraki-homeassistant/commit/8bf11a1c23ae0737a8fd4ee10a865c9dd2a2b20a))
* Correctly instantiate MerakiOptionsFlowHandler ([6bc4eec](https://github.com/brewmarsh/meraki-homeassistant/commit/6bc4eec0bb1179b220d05b5a77109acc49207874))
* **device_info:** Correctly resolve client devices and reduce warnings ([c24f361](https://github.com/brewmarsh/meraki-homeassistant/commit/c24f3611f5d6b75776a73e62ee74611a8bbf7caf))
* **logging:** Improve error handling and remove diagnostic logs ([dcc14f9](https://github.com/brewmarsh/meraki-homeassistant/commit/dcc14f92e1839ad37bd5dbec1b7701505a434b1e))
* Remove appliance firewall logic for stability ([cf7955a](https://github.com/brewmarsh/meraki-homeassistant/commit/cf7955aeb6cf9438e14bef8edcfbf1b265352b43))
* **web_server:** Correct bugs in parental controls API ([7f96f45](https://github.com/brewmarsh/meraki-homeassistant/commit/7f96f456655432d22002d57feb4a0f93337f606b))


### Features

* Add debug logging to parental controls setup ([f5f6332](https://github.com/brewmarsh/meraki-homeassistant/commit/f5f63326d1c53c67930429e2727108207c0ad032))
* Implement Parental Controls feature ([18ba72c](https://github.com/brewmarsh/meraki-homeassistant/commit/18ba72cd4822e90703c53596ccedf9d44c1e1cc8))
* Implement UI redesign, settings page, and E2E tests ([f58b061](https://github.com/brewmarsh/meraki-homeassistant/commit/f58b0615fd9bec62450bebe78865475946c59131))
* Implement web UI, filtering, and E2E tests ([da52450](https://github.com/brewmarsh/meraki-homeassistant/commit/da52450fd959981b50fb65afde7d010337982ff2))
* Improve documentation and HACS integration structure ([0d530ff](https://github.com/brewmarsh/meraki-homeassistant/commit/0d530ff1b28a12e2f7f5e46fb2c7911b74fa018e))
* Improve documentation and HACS integration structure ([c041c76](https://github.com/brewmarsh/meraki-homeassistant/commit/c041c76a5621e671f5f30f46b0ba974074897bf8))
* Major Overhaul, New Features, and Design Docs ([3398318](https://github.com/brewmarsh/meraki-homeassistant/commit/339831880dfed3771aea3f66bbd0986d4521cfcc))
* Organize documentation into a docs directory ([281d59c](https://github.com/brewmarsh/meraki-homeassistant/commit/281d59c73e3c59a360ad9a3950ee6e6fae9d71f0))
* **parental_controls:** Add SSID-specific firewall rule handling ([04d631a](https://github.com/brewmarsh/meraki-homeassistant/commit/04d631ac562ded38b3aa21f6b75e193dafcc9414))
* Redesign web UI and fix test suite ([a40b4a1](https://github.com/brewmarsh/meraki-homeassistant/commit/a40b4a128c5fdf7ecb9c4e5abc90285de4c6cdfb))
* Redesign web UI with new layout and theme ([fe07f71](https://github.com/brewmarsh/meraki-homeassistant/commit/fe07f7183d735636bde105192bf274a59507ada2))
* Refactor Parental Controls and enhance with blocked categories ([5b0f202](https://github.com/brewmarsh/meraki-homeassistant/commit/5b0f202b6050ed1847497942290aa29f72f60de4))
* Refactor Parental Controls for per-SSID and network-wide support ([3056f1f](https://github.com/brewmarsh/meraki-homeassistant/commit/3056f1fb1ed1b7d6b9e1ba233bc79121e97fb66f))
* **ui:** Implement frontend for granular parental controls ([af3ccbe](https://github.com/brewmarsh/meraki-homeassistant/commit/af3ccbe2e0ae110c8c532e6c15a8f9d3998c46ba))



## [1.4.2](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.4.1...v1.4.2) (2025-08-20)



## [1.4.1](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.4.0...v1.4.1) (2025-08-14)



# [1.4.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.3.0...v1.4.0) (2025-08-14)



# [1.3.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.2.3...v1.3.0) (2025-08-14)


### Bug Fixes

* Correct MV audio detection toggle functionality ([f0c82cc](https://github.com/brewmarsh/meraki-homeassistant/commit/f0c82cc2c9a095414b80bdd1578da6dc6443abbe))
* Correct MV Sense toggle functionality ([c749987](https://github.com/brewmarsh/meraki-homeassistant/commit/c749987b313992c087f5f853340bc880251eb97e))
* Remove unused imports ([20a391c](https://github.com/brewmarsh/meraki-homeassistant/commit/20a391ccfa6fc95e0c730f012d8eb7629f4e61be))
* Remove unused imports from sensor_registry ([2a175aa](https://github.com/brewmarsh/meraki-homeassistant/commit/2a175aac91477703dbe9c30cc9a20daa875a5b2b))
* Resolve multiple mypy errors and a TypeError ([1b7f1a3](https://github.com/brewmarsh/meraki-homeassistant/commit/1b7f1a3fcae3a333201c1e5d46dcd6ff405ace4c))


### Features

* Disable RTSP for MV2 cameras ([0f501df](https://github.com/brewmarsh/meraki-homeassistant/commit/0f501dfdc5f386283ffd6b323e0ef64d60b3e8cf))



## [1.2.3](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.2.2...v1.2.3) (2025-08-14)


### Features

* Generate system requirements document ([d789377](https://github.com/brewmarsh/meraki-homeassistant/commit/d789377e8e64a2fcdfc5bf1771ba73e597a71442))



## [1.2.2](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.2.1...v1.2.2) (2025-08-13)


### Bug Fixes

* consolidate and correct the versioning workflow ([1cf9bb7](https://github.com/brewmarsh/meraki-homeassistant/commit/1cf9bb7c2b912671e9fa50cc32afc9c88638b510))



## [1.2.1](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.2.0...v1.2.1) (2025-08-13)


### Bug Fixes

* Add logging and re-verify options flow and name formatting ([1ca417c](https://github.com/brewmarsh/meraki-homeassistant/commit/1ca417ce266fd3de0c3f000d5771a7fea25ec35c))
* Address multiple regressions ([538a7bc](https://github.com/brewmarsh/meraki-homeassistant/commit/538a7bcff7febc4ada51b855c02a7cec62a9ab69))
* Address multiple regressions ([f2e63af](https://github.com/brewmarsh/meraki-homeassistant/commit/f2e63af68fd276652e4c7e3fb478643109653a9a))
* Address multiple regressions ([3947218](https://github.com/brewmarsh/meraki-homeassistant/commit/3947218d1bbd80a4f98eb64b8b682e131a091cab))
* Address options flow and device name formatting issues ([a2d905c](https://github.com/brewmarsh/meraki-homeassistant/commit/a2d905c24a558fa284ff473138dac91e42b91ea9))
* Address regressions from previous commit ([cad0041](https://github.com/brewmarsh/meraki-homeassistant/commit/cad0041b0ffb1f3e784fa44e52955f2fbbd91bcc))
* Address various bugs and add new features ([528768e](https://github.com/brewmarsh/meraki-homeassistant/commit/528768ec6de6c35bd145deefcfcc1cb121e8d381))
* Address various bugs and update documentation ([ab423bc](https://github.com/brewmarsh/meraki-homeassistant/commit/ab423bc97d13909aaf1f7197e0a37cf425a646f0))
* consolidate and correct the versioning workflow ([ecadeca](https://github.com/brewmarsh/meraki-homeassistant/commit/ecadeca99275acbc247731345df0b08f52f91da1))
* Correct API call for enabling RTSP stream ([98d2746](https://github.com/brewmarsh/meraki-homeassistant/commit/98d27463b09d1fcd8de394a9d7d144e50d3ffd13))
* Correct API call for getting appliance uplinks settings ([3ff48c2](https://github.com/brewmarsh/meraki-homeassistant/commit/3ff48c2b0de794184ee8684eb4ac247276c0175e))
* Correct API call for getting sensor readings ([e3eb39b](https://github.com/brewmarsh/meraki-homeassistant/commit/e3eb39b406a8ee7e3edbc30b58588c29535d830e))
* Correct auto-enable RTSP logic for cameras ([0f69245](https://github.com/brewmarsh/meraki-homeassistant/commit/0f69245e1b1a7ba9aad45b679e459c85ddee553e))
* Correct connected clients sensor for all device types ([5213c94](https://github.com/brewmarsh/meraki-homeassistant/commit/5213c9437e40f2e9ea97dadacf8fe038833245ea))
* Correct data handling for appliance sensors ([c6610ea](https://github.com/brewmarsh/meraki-homeassistant/commit/c6610eae19bbe2c756695f935009895e77c6d282))
* Correct device tracker lifecycle and naming ([9eab0d5](https://github.com/brewmarsh/meraki-homeassistant/commit/9eab0d53da815dd81121d89b89b7a9543d081fea))
* Correct import error and update documentation ([2f6f676](https://github.com/brewmarsh/meraki-homeassistant/commit/2f6f67623599d63bb788d9c75e90d676b2b30e0f))
* correct import statement in organization.py ([41d76da](https://github.com/brewmarsh/meraki-homeassistant/commit/41d76daab74b57927507c385e35b21e01a7dac79))
* Correct IndentationError in org_device_type_clients.py ([e04d0c0](https://github.com/brewmarsh/meraki-homeassistant/commit/e04d0c00fe32d64a6e36035e2d9b366bd6261fab))
* Correct Meraki API method names in coordinator ([a3036c4](https://github.com/brewmarsh/meraki-homeassistant/commit/a3036c44d723e95c4b01d68643a452045ac41049))
* Correct platform unloading on reconfigure ([f650a13](https://github.com/brewmarsh/meraki-homeassistant/commit/f650a13cdcb0b43e84d8398093771b4c4634773a))
* Correct RTSP auto-enable logic for cameras ([bcec7ec](https://github.com/brewmarsh/meraki-homeassistant/commit/bcec7ec8839db0148b3c00e4f56c074fc330ae11))
* Correct SSID filtering and apply entity icons ([1680107](https://github.com/brewmarsh/meraki-homeassistant/commit/1680107c342c1775cbd65fa7fff033c88c6c9d0d))
* correct state_class for data_usage sensor ([0fa94d3](https://github.com/brewmarsh/meraki-homeassistant/commit/0fa94d3d83c4108449bbff3f3309fbe0304cf214))
* Correctly call `async_add_executor_job` with keyword arguments ([caf3fad](https://github.com/brewmarsh/meraki-homeassistant/commit/caf3fad6d306fea1fec405a5bcffe4cfc5c01c8c))
* Correctly retrieve auto_enable_rtsp option ([74028e3](https://github.com/brewmarsh/meraki-homeassistant/commit/74028e379063d48353ae62481e8d6f873040d21d))
* Ensure consistent device name formatting for all entities ([a2b2c5a](https://github.com/brewmarsh/meraki-homeassistant/commit/a2b2c5ae52d0f5c8b897c8f0c603f28892e8ed8f))
* Ensure consistent SSID device representation ([6b5083e](https://github.com/brewmarsh/meraki-homeassistant/commit/6b5083e1fda838f2695d434a59f5742d560c9756))
* explicitly set current_version in bumpversion config ([9bca6b3](https://github.com/brewmarsh/meraki-homeassistant/commit/9bca6b3fbe5d809411a5bf6ce205cf428d43c338))
* Final round of fixes for options flow and device naming ([a02e947](https://github.com/brewmarsh/meraki-homeassistant/commit/a02e947f290524ec53a82a96d07ac2eb9a95c140))
* Finalize appliance sensor refactoring and cleanup ([604f57b](https://github.com/brewmarsh/meraki-homeassistant/commit/604f57bd7043b65e343b47a76f1b4c976e8f5b73))
* fix import error and improve code quality ([a3cde58](https://github.com/brewmarsh/meraki-homeassistant/commit/a3cde58833a0bdf068f68639173e3a9e186abe4b))
* Improve Data Usage sensor state and add documentation ([53ce207](https://github.com/brewmarsh/meraki-homeassistant/commit/53ce2071e7f0919e7b53ef1d4d0e87b5b08afbe7))
* Improve RTSP URL handling and add more logging ([3002aa0](https://github.com/brewmarsh/meraki-homeassistant/commit/3002aa0cf20f3fb52f2e73a924f1f3a8c878ef7e))
* Inject networkId into SSID data ([1113646](https://github.com/brewmarsh/meraki-homeassistant/commit/11136461ed157ddaf8b72a84a46a657ce36b4c7e))
* Make SSID filtering case-insensitive ([199d7b0](https://github.com/brewmarsh/meraki-homeassistant/commit/199d7b0aff2f0abbbbf761ed6573f47f7c68f54b))
* Pass options to coordinators to fix auto-enable RTSP ([e40aa51](https://github.com/brewmarsh/meraki-homeassistant/commit/e40aa51195a7b635663e1ba913440e5014730d98))
* Prevent crash if traffic analysis is disabled ([626c45e](https://github.com/brewmarsh/meraki-homeassistant/commit/626c45e69e23c73fa257981f87e1a15e8ad88a6f))
* Rebuild options flow and fix camera naming and RTSP URL ([6549f5f](https://github.com/brewmarsh/meraki-homeassistant/commit/6549f5f759f1ad677bcbfc2193b49656cd64fd17))
* Refine entity naming and fix camera processing ([343b49f](https://github.com/brewmarsh/meraki-homeassistant/commit/343b49fc7285752850685c23e3bebb6141e10f5a))
* remove token from codecov badge URL ([b4c7b32](https://github.com/brewmarsh/meraki-homeassistant/commit/b4c7b3264aaa707142c47e15473ea404512c03e6))
* Resolve AttributeError during authentication ([2e2f94b](https://github.com/brewmarsh/meraki-homeassistant/commit/2e2f94bc0f07210010911d5cb5e34e1bdcb07aaa))
* Resolve AttributeError for camera entities ([5af7b05](https://github.com/brewmarsh/meraki-homeassistant/commit/5af7b05acc72fc8fdfdba0e38dda8b450766572b))
* Resolve AttributeError on close during authentication ([28c2bf0](https://github.com/brewmarsh/meraki-homeassistant/commit/28c2bf040db19ca68fe757e1dce75ea7c82cb125))
* Resolve AttributeError when fetching device uplink ([d77befe](https://github.com/brewmarsh/meraki-homeassistant/commit/d77befe794cbf43c596fc47225f5741ca96bbb1a))
* Resolve multiple flake8 linting errors ([634e997](https://github.com/brewmarsh/meraki-homeassistant/commit/634e997904b7749287010f6cb86616c1464ca359))
* Resolve uplink attribute error and duplicate unique IDs ([f89dea9](https://github.com/brewmarsh/meraki-homeassistant/commit/f89dea98880e1aace4af59830f89e33e9586af71))
* Resolve various errors ([7b8eedf](https://github.com/brewmarsh/meraki-homeassistant/commit/7b8eedf18791a637af835dc43aa3f289c094066d))
* Resolve various errors ([54e1cce](https://github.com/brewmarsh/meraki-homeassistant/commit/54e1cce121ebebbb1335e745b4dd0191cb37538b))
* Resolve various errors and duplicate unique IDs ([11deaa4](https://github.com/brewmarsh/meraki-homeassistant/commit/11deaa4fef49535358288b63e9ace3938055595e))
* Resolve various errors and typos ([dfe4cb1](https://github.com/brewmarsh/meraki-homeassistant/commit/dfe4cb1e4c387943be22d36cf2d46b154fe37135))
* Resolve various errors and update documentation ([2ac0e43](https://github.com/brewmarsh/meraki-homeassistant/commit/2ac0e430af8d01aa84a99fc0d9a967342b8cb94d))
* Revert incorrect change to get_organization_device_statuses ([213c293](https://github.com/brewmarsh/meraki-homeassistant/commit/213c2938e3a741511db10e64ebb6b337b18f377b))
* **sensor:** Add missing helper method to DataUsage sensor ([73e12ff](https://github.com/brewmarsh/meraki-homeassistant/commit/73e12ff60bea9486c018c5a3e7ec9f197376f98f))
* update deprecated actions/upload-artifact and actions/download-artifact to v4 ([d16e468](https://github.com/brewmarsh/meraki-homeassistant/commit/d16e468bb26af281e642c41397c59eada41c1bef))
* Use 'visible' attribute for SSID broadcast switch ([b813f3c](https://github.com/brewmarsh/meraki-homeassistant/commit/b813f3c6748b42fab81655c1bc8b4adea0aca8c3))
* use bumpversion instead of bump2version in release workflow ([462fb43](https://github.com/brewmarsh/meraki-homeassistant/commit/462fb433cb502f43abecdfd1c923accd60442d23))
* Use MerakiDataUpdateCoordinator and add linting ([1f0d9d8](https://github.com/brewmarsh/meraki-homeassistant/commit/1f0d9d86c3dd90ece3f7610b7fe35d8a08289466))
* Use MerakiDataUpdateCoordinator and add linting ([aa0be8b](https://github.com/brewmarsh/meraki-homeassistant/commit/aa0be8b8ce51cf4c6bf1aa3a40ce8ce77bcd5864))
* Use MerakiDataUpdateCoordinator in __init__.py ([cb38a8b](https://github.com/brewmarsh/meraki-homeassistant/commit/cb38a8b086b9cf243aa996cfe798d7378c65912c))


### Features

* Add additional detail sensors for SSIDs ([7ab56e4](https://github.com/brewmarsh/meraki-homeassistant/commit/7ab56e4287bcd17b5143b1fb55b1f410e0ddb10e))
* Add appliance hostname to device details ([0d0fe4c](https://github.com/brewmarsh/meraki-homeassistant/commit/0d0fe4c8d84d44339fc49c14c15705fd74df306a))
* Add appliance uplink status sensors ([e05c38f](https://github.com/brewmarsh/meraki-homeassistant/commit/e05c38feb001652d8260f98c5fb2b0e306441bb7))
* Add camera support and improve configuration ([dbbd4d6](https://github.com/brewmarsh/meraki-homeassistant/commit/dbbd4d6c617a606a76cdeb9e3596272d86e8ff0e))
* Add camera support and improve configuration ([4b6e534](https://github.com/brewmarsh/meraki-homeassistant/commit/4b6e534a24185d8554142d1f0dc39f3256004680))
* Add camera support and improve configuration ([7cebd3f](https://github.com/brewmarsh/meraki-homeassistant/commit/7cebd3fe36f5d0fc717fca353cf73f20e369ddc1))
* Add camera support and improve configuration ([015d620](https://github.com/brewmarsh/meraki-homeassistant/commit/015d6208412709115dc26357b09543b474fc2621))
* Add camera support and improve configuration ([d1cce3a](https://github.com/brewmarsh/meraki-homeassistant/commit/d1cce3a41ff8aa6b360d680c3d225eaf68b70481))
* Add camera support and improve configuration ([ff29ec0](https://github.com/brewmarsh/meraki-homeassistant/commit/ff29ec0b994dcfa861c7f969af4ad9f49d1d4307))
* Add camera support and improve configuration ([32fb3a6](https://github.com/brewmarsh/meraki-homeassistant/commit/32fb3a6cd1b1336345926d5e1355e5d103baff13))
* Add camera support and improve configuration ([f6315af](https://github.com/brewmarsh/meraki-homeassistant/commit/f6315aff9e0a33d0027433017afb1639cbc47ab0))
* Add code coverage reporting ([5ec5c40](https://github.com/brewmarsh/meraki-homeassistant/commit/5ec5c405758529faeed0bcbc4e70273b622d6b0c))
* Add code coverage reporting ([aa90c79](https://github.com/brewmarsh/meraki-homeassistant/commit/aa90c791e9fc2596d758f640ebb5eba0fa850413))
* Add code coverage reporting ([85a1c35](https://github.com/brewmarsh/meraki-homeassistant/commit/85a1c356ac24b10378200d4952355a9d173267d0))
* Add device type icons ([2f7b6f1](https://github.com/brewmarsh/meraki-homeassistant/commit/2f7b6f1484fa63fde76a65ac9d5551e601a7529e))
* Add extensive logging to camera entity for debugging ([a7c781f](https://github.com/brewmarsh/meraki-homeassistant/commit/a7c781f2dabbb0cc91857b651c122f93a7187bda))
* Add option to enable/disable device tracker with UI labels ([c961597](https://github.com/brewmarsh/meraki-homeassistant/commit/c9615972b49913656c7a5bd654f6db6f6b9fdf90))
* add security scanning and requirements ([22cc269](https://github.com/brewmarsh/meraki-homeassistant/commit/22cc269a08969f57e52c99334e88dea4b2652623))
* add security scanning and requirements ([5a20c8f](https://github.com/brewmarsh/meraki-homeassistant/commit/5a20c8f8804757ea9599d576c601fbc7f5aaa64e))
* Add SSID filter logging and update AGENTS.md ([f6bb024](https://github.com/brewmarsh/meraki-homeassistant/commit/f6bb0246447853ed75fe4b024233dc66ee75134d))
* Audit and fix all device sensors ([67ae4fe](https://github.com/brewmarsh/meraki-homeassistant/commit/67ae4fee53ba14b01f98ba38caae7eb4c3daec13))
* Audit and fix all device sensors ([9aff2eb](https://github.com/brewmarsh/meraki-homeassistant/commit/9aff2ebed818a4cf8d4b0920f6c79e5036f9a095))
* Filter out unconfigured SSIDs ([a61a889](https://github.com/brewmarsh/meraki-homeassistant/commit/a61a88998dbb957d4d9e719ed865558922413dba))
* fix build system and add security scanning ([2178d50](https://github.com/brewmarsh/meraki-homeassistant/commit/2178d505fc3e372fa9c723eb1f17d2a038f85714))
* fix build system and improve code quality ([cef46e8](https://github.com/brewmarsh/meraki-homeassistant/commit/cef46e805c1930f22573edb42c1b22b7d594f327))
* Implement and fix all outstanding requirements ([fe4f526](https://github.com/brewmarsh/meraki-homeassistant/commit/fe4f5263f2e9f954fc2ee069f07f83f8bd1897cb))
* Implement and fix requirements from requirements.md ([8b9b7fe](https://github.com/brewmarsh/meraki-homeassistant/commit/8b9b7fe78924b10d8951c128d0d312683272eff0))
* Implement comprehensive CI/CD and release process improvements ([a2c6754](https://github.com/brewmarsh/meraki-homeassistant/commit/a2c6754e3b030628fdaaaf2b5f0bc8c614b63280))
* Implement comprehensive CI/CD and release process improvements ([74b3488](https://github.com/brewmarsh/meraki-homeassistant/commit/74b34887bf54127c05415c5d6ce2428e61ec0889))
* Implement updatable SSID names via Text entity ([8009822](https://github.com/brewmarsh/meraki-homeassistant/commit/80098222bafb15e0c2c9066e66a2699bca32acc9))
* Implement updatable SSID names via Text entity ([c5ad7ef](https://github.com/brewmarsh/meraki-homeassistant/commit/c5ad7ef7242efdb457e3e290e9a2cc8049b5ac62))
* improve build system and release process ([61a9060](https://github.com/brewmarsh/meraki-homeassistant/commit/61a906035928c3e8950009bc5b592b91b4994a9d))
* improve build system and release process ([171b81e](https://github.com/brewmarsh/meraki-homeassistant/commit/171b81e5491efa8bfb16cdb05e3c056f15a02b92))
* improve code quality and fix tests ([5e6be6d](https://github.com/brewmarsh/meraki-homeassistant/commit/5e6be6d7ac4a4b26659b934967a9c3af75e00a7a))
* Improve device info and add appliance port sensors ([c93c96b](https://github.com/brewmarsh/meraki-homeassistant/commit/c93c96bc9e2d18481119eac7220065890f7155ae))
* Improve sensor state when traffic analysis is disabled ([fbb7907](https://github.com/brewmarsh/meraki-homeassistant/commit/fbb79073d5173e539a0950e6d544e0d4cd311282))
* Improve user-friendliness of configuration options ([8c4b565](https://github.com/brewmarsh/meraki-homeassistant/commit/8c4b56537f80475abb90a96cc0ffec71224a450a))
* Refactor Device Tracker to Client Sensor Platform ([f0b2823](https://github.com/brewmarsh/meraki-homeassistant/commit/f0b282334e9e6c396a1f65d6d2ef67e3d1c41617))
* Refactor switch port sensors ([afad9ba](https://github.com/brewmarsh/meraki-homeassistant/commit/afad9ba07c59a646cebffe7a9f5581faca4fb303))
* Update docs and add optional webhook URL ([edce3f4](https://github.com/brewmarsh/meraki-homeassistant/commit/edce3f422dfc84c575496630c541f62d56e4e4a6))



# [1.2.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.1.0...v1.2.0) (2025-07-10)



# [1.1.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v1.0.0...v1.1.0) (2025-07-10)



# [1.0.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.9.0...v1.0.0) (2025-07-09)



# [0.9.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.8.1...v0.9.0) (2025-07-01)



## [0.8.1](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.8.0...v0.8.1) (2025-06-11)



# [0.8.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.7.0...v0.8.0) (2025-06-09)


### Bug Fixes

* Correct availability check for RTSP camera switch ([7dc635a](https://github.com/brewmarsh/meraki-homeassistant/commit/7dc635a24fc48d61141720cdb5b7ea62a85e789d))
* Ensure consistent use of `externalRtspEnabled` for RTSP ([d2f4cc2](https://github.com/brewmarsh/meraki-homeassistant/commit/d2f4cc2c48ac843519354be1dd68fcf3306bf134))
* Preserve rtspServerEnabled key during data processing ([00bedac](https://github.com/brewmarsh/meraki-homeassistant/commit/00bedacb224aefc8c2094aadf122d252a6d99b6b))


### Features

* Add RTSP stream control switch for Meraki cameras ([e0d7395](https://github.com/brewmarsh/meraki-homeassistant/commit/e0d7395c0506385d21440a310b0c68b2a0644bef))
* Add sensor for Meraki camera RTSP stream URL ([2399452](https://github.com/brewmarsh/meraki-homeassistant/commit/23994525be73df90daf9f414aa1ad84a111d32b4))



# [0.7.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.6.0...v0.7.0) (2025-06-09)



# [0.6.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.5.1...v0.6.0) (2025-06-06)



## [0.5.1](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.5.0...v0.5.1) (2025-06-06)



# [0.5.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.4.2...v0.5.0) (2025-06-06)



## [0.4.2](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.4.1...v0.4.2) (2025-06-06)



## [0.4.1](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.4.0...v0.4.1) (2025-06-05)



# [0.4.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.3.0...v0.4.0) (2025-06-05)



# [0.3.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.2.0...v0.3.0) (2025-06-05)


### Bug Fixes

* Improve naming consistency and add diagnostics ([31c7fde](https://github.com/brewmarsh/meraki-homeassistant/commit/31c7fde03ccd248015fd2041c86232e6eacc9b14))


### Features

* Add Organization device, org-wide client sensors, and naming/logging improvements ([5eaa50f](https://github.com/brewmarsh/meraki-homeassistant/commit/5eaa50f10517498d31d2f957b4689ac6a6d7834e))



# [0.2.0](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.1.2...v0.2.0) (2025-06-04)



## [0.1.2](https://github.com/brewmarsh/meraki-homeassistant/compare/v0.1.1...v0.1.2) (2025-06-04)



# 0.1.0 (2025-05-26)


### Features

* Comprehensive documentation and build system update ([5c553b4](https://github.com/brewmarsh/meraki-homeassistant/commit/5c553b4c2873f9720c5190641f750fa06e2d78b4))



## 0.0.3 (2025-04-04)



# Meraki for Home Assistant Changelog

## 1.2.0

- Add an apparmor profile
- Update to 3.15 base image with s6 v3
- Add a sample script to run as service and constrain in aa profile

## 1.1.0

- Updates

## 1.0.0

- Initial release
