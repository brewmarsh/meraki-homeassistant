"""Core API package."""

from __future__ import annotations

from .factory import create_api_client
from .protocol import MerakiApiClientProtocol

__all__ = ["create_api_client", "MerakiApiClientProtocol"]
