"""Search operations for IMA API."""

from typing import Any

from .client import ImaClient


class SearchAPI:
    """Search operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def search_knowledge(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
        knowledge_base_id: str = "",
        **kwargs,
    ) -> dict[str, Any]:
        """
        Search knowledge items by keyword.

        Args:
            keyword: Search query
            page: Page number
            page_size: Results per page
            knowledge_base_id: Limit search to a specific knowledge base
        """
        payload: dict[str, Any] = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
        }
        if knowledge_base_id:
            payload["knowledge_base_id"] = knowledge_base_id
        payload.update(kwargs)
        return self.client.post("knowledge/search_knowledge", payload)

    def get_knowledge_sug(self, keyword: str, **kwargs) -> dict[str, Any]:
        """Get search suggestions for a keyword."""
        payload: dict[str, Any] = {"keyword": keyword}
        payload.update(kwargs)
        return self.client.post("knowledge/get_knowledge_sug", payload)

    def is_knowledge_exist(self, source_url: str) -> dict[str, Any]:
        """Check if knowledge with given URL already exists."""
        return self.client.post(
            "knowledge/is_knowledge_exist", {"source_url": source_url}
        )
