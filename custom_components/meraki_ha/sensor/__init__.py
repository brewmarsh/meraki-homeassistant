# custom_components/meraki_ha/sensor/__init__.py
"""Meraki HA Sensor Entities.

This file makes the 'sensor' directory a Python package.
It should not contain platform setup logic if custom_components/meraki_ha/sensor.py
is the main entry point for the sensor platform.
"""
_LOGGER = logging.getLogger(__name__) # Added to address F821 in original file, though content is mostly removed
# Ensure logging is imported if used, even if minimally.
import logging
