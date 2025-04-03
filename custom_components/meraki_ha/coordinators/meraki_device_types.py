"""Utility functions for Meraki device types."""


def map_meraki_model_to_device_type(model: str) -> str:
    """Maps a Meraki device model to a generic device type."""
    if model.startswith("MR") or model.startswith("GR"):
        return "Wireless"
    elif model.startswith("MS") or model.startswith("GS"):
        return "Switch"
    elif model.startswith("MX"):
        return "Appliance"
    elif model.startswith("MV"):
        return "Camera"
    elif model.startswith("MT"):
        return "Sensor"
    else:
        return "Unknown"
