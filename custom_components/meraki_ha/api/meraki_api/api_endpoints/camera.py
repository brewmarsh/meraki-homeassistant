from typing import TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from .._api_client import MerakiAPIClient


class Camera:
    """Mock for camera endpoint."""

    def __init__(self, client: "MerakiAPIClient"):
        self._client = client

    async def getDeviceCameraVideoSettings(self, serial: str) -> Dict[str, Any]:
        """Mock for getDeviceCameraVideoSettings."""
        return await self._client.get_device_camera_video_settings(serial)

    async def updateDeviceCameraVideoSettings(
        self, serial: str, **kwargs
    ) -> Dict[str, Any]:
        """Mock for updateDeviceCameraVideoSettings."""
        return await self._client.update_device_camera_video_settings(
            serial=serial, **kwargs
        )
