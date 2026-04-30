"""Knowledge CRUD operations for IMA API."""

from typing import Any, Optional, List

from .client import ImaClient


class KnowledgeAPI:
    """Knowledge item CRUD operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def get_knowledge(self, media_id: str) -> dict:
        """Get a single knowledge item by ID."""
        return self.client.post("knowledge/get_knowledge", {"media_id": media_id})

    def del_knowledge(self, media_id: str) -> dict:
        """Delete a knowledge item."""
        return self.client.post("knowledge/del_knowledge", {"media_id": media_id})

    def get_knowledge_list(
        self,
        limit: int = 20,
        offset: int = 0,
        sort_type: int = 0,
    ) -> dict:
        """
        Get paginated list of knowledge items.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            sort_type: Sort order (0=newest first, 1=oldest first)
        """
        payload = {
            "limit": limit,
            "offset": offset,
            "sort_type": sort_type,
        }
        return self.client.post("knowledge/get_knowledge_list", payload)
