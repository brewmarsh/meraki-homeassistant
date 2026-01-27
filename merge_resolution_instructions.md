To resolve this merge conflict in your local environment, you need to manually edit the file that contains this conflict. Based on the code snippet, this conflict is likely in `custom_components/meraki_ha/core/api/client.py`.

Here's how you can resolve it:

1.  Open the file `custom_components/meraki_ha/core/api/client.py` in your text editor.
2.  Locate the section with the merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
3.  Replace the entire conflicting section with the following resolved code:

```python
        self._hass = hass
        self._base_url = base_url

        self.dashboard = meraki.DashboardAPI(
            api_key=self._api_key,
            base_url=self._base_url,
        )

        # Initialize endpoint handlers
        self.appliance = ApplianceEndpoints(self, self._hass)
        self.camera = CameraEndpoints(self)
        self.devices = DevicesEndpoints(self)
        self.network = NetworkEndpoints(self)
        self.organization = OrganizationEndpoints(self)
        self.switch = SwitchEndpoints(self)
        self.wireless = WirelessEndpoints(self)
        self.sensor = SensorEndpoints(self)

        # Semaphore to limit concurrent API calls
        self._semaphore = asyncio.Semaphore(2)

        # Set of disabled features to prevent repetitive API calls
        self._disabled_features: set[str] = set()
```

4.  After saving the file, you need to stage the change using `git add custom_components/meraki_ha/core/api/client.py`.
5.  Then, you can continue your merge (e.g., `git merge --continue` if you were in the middle of a merge, or `git commit` if it was a rebase).

This resolution integrates the endpoint handlers and features from the `fix/wireless-ipsk-crash-14368601733312930129` branch while retaining the direct initialization of `meraki.DashboardAPI` from your `beta` branch, which seems to be the intended approach.
