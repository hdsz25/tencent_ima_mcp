"""Authentication management for IMA API."""

from .client import ImaClient


class AuthManager:
    """Manages authentication state for IMA API."""

    def __init__(self, client: ImaClient):
        self.client = client

    def refresh(self) -> bool:
        """Manually trigger token refresh."""
        return self.client._refresh_token()

    def is_authenticated(self) -> bool:
        """Check if we have valid credentials loaded."""
        return bool(self.client.user_id and self.client.token)

    def get_user_info(self) -> dict:
        """Get current user info from config."""
        return {
            "user_id": self.client.user_id,
            "has_token": bool(self.client.token),
            "has_refresh_token": bool(self.client.refresh_token),
        }
