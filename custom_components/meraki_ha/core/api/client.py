    async def get_network_events(
        self,
        network_id: str,
        product_type: str | None = None,
        included_event_types: list[str] | None = None,
        excluded_event_types: list[str] | None = None,
        device_serial: str | None = None,
        device_mac: str | None = None,
        client_ip: str | None = None,
        client_mac: str | None = None,
        client_name: str | None = None,
        sm_device_mac: str | None = None,
        sm_device_name: str | None = None,
        per_page: int | None = None,
        starting_after: str | None = None,
        ending_before: str | None = None,
    ) -> dict[str, Any]:
        """
        Fetch events for a network.

        Args:
            network_id: The ID of the network.
            product_type: Filter events by product type.
            included_event_types: Filter events by included event types.
            excluded_event_types: Filter events by excluded event types.
            device_serial: Filter events by device serial.
            device_mac: Filter events by device MAC.
            client_ip: Filter events by client IP.
            client_mac: Filter events by client MAC.
            client_name: Filter events by client name.
            sm_device_mac: Filter events by SM device MAC.
            sm_device_name: Filter events by SM device name.
            per_page: Number of events per page.
            starting_after: Token for next page.
            ending_before: Token for previous page.

        Returns:
            A dictionary containing the events and next page token.
        """
        return await self._run_with_semaphore(
             self.run_sync(
                self.dashboard.networks.getNetworkEvents,
                network_id,
                productType=product_type,
                includedEventTypes=included_event_types,
                excludedEventTypes=excluded_event_types,
                deviceSerial=device_serial,
                deviceMac=device_mac,
                clientIp=client_ip,
                clientMac=client_mac,
                clientName=client_name,
                smDeviceMac=sm_device_mac,
                smDeviceName=sm_device_name,
                perPage=per_page,
                startingAfter=starting_after,
                endingBefore=ending_before,
            )
        )
