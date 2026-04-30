"""Media/file upload operations for IMA API."""

from typing import Any

from .client import ImaClient


class MediaAPI:
    """Media and file upload operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def create_media(
        self, file_name: str, file_size: int, file_type: str = "", **kwargs
    ) -> dict[str, Any]:
        """
        Create a media entry (pre-upload registration).

        Args:
            file_name: Name of the file
            file_size: Size of the file in bytes
            file_type: MIME type of the file
        """
        payload: dict[str, Any] = {
            "file_name": file_name,
            "file_size": file_size,
        }
        if file_type:
            payload["file_type"] = file_type
        payload.update(kwargs)
        return self.client.post("media/create_media", payload)

    def get_media(self, media_id: str) -> dict[str, Any]:
        """Get media details by ID."""
        return self.client.post("media/get_media", {"media_id": media_id})

    def get_simple_media(self, media_id: str) -> dict[str, Any]:
        """Get simplified media info."""
        return self.client.post("media/get_simple_media", {"media_id": media_id})

    def get_upload_credential(self, **kwargs) -> dict[str, Any]:
        """Get upload credential (temporary token for direct upload)."""
        return self.client.post("media/get_upload_credential", kwargs or {})

    def get_upload_credential_by_media(self, media_id: str, **kwargs) -> dict[str, Any]:
        """Get upload credential for a specific media entry."""
        payload: dict[str, Any] = {"media_id": media_id}
        payload.update(kwargs)
        return self.client.post("media/get_upload_credential_by_media", payload)

    def delete_temp_media(self, media_id: str) -> dict[str, Any]:
        """Delete a temporary media entry."""
        return self.client.post("media/delete_temp_media", {"media_id": media_id})

    def cancel_upload_media(self, media_id: str) -> dict[str, Any]:
        """Cancel an in-progress media upload."""
        return self.client.post("media/cancel_upload_media", {"media_id": media_id})
