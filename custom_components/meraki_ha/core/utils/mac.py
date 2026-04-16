"""MAC address utilities for Meraki integration."""

from __future__ import annotations


def is_locally_administered_mac(mac: str) -> bool:
    """
    Check if a MAC address is locally administered (potentially randomized).

    The second character of the MAC address represents the locally administered bit.
    Hex digits 2, 3, 6, 7, A, B, E, F have the locally administered bit set.

    Args:
    ----
        mac: The MAC address to check (e.g., '00:11:22:33:44:55' or '001122334455').

    Returns
    -------
        True if the MAC address is locally administered, False otherwise.

    """
    if not mac:
        return False

    # Remove non-hex characters
    clean_mac = "".join(c for c in mac if c.isalnum())

    if len(clean_mac) < 2:
        return False

    # Get the second hex digit
    second_char = clean_mac[1].upper()

    # Check if bit 1 of the first octet is set
    # The hex digit Y in XY:xx... represents bits 3, 2, 1, 0.
    # Bit 1 is the locally administered bit.
    return second_char in ("2", "3", "6", "7", "A", "B", "E", "F")
