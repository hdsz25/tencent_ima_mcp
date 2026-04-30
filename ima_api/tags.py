"""Tag management operations for IMA API."""

from typing import List

from .client import ImaClient


class TagsAPI:
    """Tag management operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def get_tags(self, limit: int = 50) -> dict:
        """Get all tags for the current user.
        
        Args:
            limit: Maximum number of tags to return (required by API)
        """
        return self.client.post("knowledge/get_tags", {"limit": limit})

    def update_tags(self, media_id: str, tags: List[str]) -> dict:
        """Update tags for a knowledge item.
        
        Args:
            media_id: The media_id of the knowledge item
            tags: List of tag names to set
        """
        return self.client.post("knowledge/update_tags", {"media_id": media_id, "tags": tags})

    def search_tags(self, keyword: str, limit: int = 20) -> dict:
        """Search tags by keyword.
        
        Args:
            keyword: Search keyword
            limit: Maximum number of results (required by API, must be > 0)
        """
        return self.client.post("knowledge/search_tags", {"keyword": keyword, "limit": limit})
