"""Search operations for IMA API."""

from .client import ImaClient


class SearchAPI:
    """Search operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def search_knowledge(self, keyword: str, limit: int = 20) -> dict:
        """
        Search knowledge items by keyword.

        Args:
            keyword: Search query
            limit: Maximum number of results
        """
        return self.client.post(
            "knowledge/search_knowledge", {"keyword": keyword, "limit": limit}
        )

    def get_knowledge_sug(self, keyword: str) -> dict:
        """Get search suggestions for a keyword."""
        return self.client.post("knowledge/get_knowledge_sug", {"keyword": keyword})
