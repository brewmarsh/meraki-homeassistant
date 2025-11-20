
@websocket_api.async_response
async def handle_get_network_events(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """
    Handle get_network_events command.

    Args:
    ----
        hass: The Home Assistant instance.
        connection: The WebSocket connection.
        msg: The WebSocket message.

    """
    config_entry_id = msg["config_entry_id"]
    network_id = msg["network_id"]
    per_page = msg.get("per_page", 10)
    starting_after = msg.get("starting_after")

    if config_entry_id not in hass.data[DOMAIN]:
        connection.send_error(msg["id"], "not_found", "Config entry not found")
        return

    coordinator: MerakiDataCoordinator = hass.data[DOMAIN][config_entry_id][
        "coordinator"
    ]

    try:
        events = await coordinator.api.get_network_events(
            network_id=network_id,
            per_page=per_page,
            starting_after=starting_after,
        )
        connection.send_result(msg["id"], events)
    except Exception as e:
        _LOGGER.error("Error fetching network events: %s", e)
        connection.send_error(msg["id"], "fetch_error", str(e))
