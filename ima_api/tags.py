"""Tag management operations for IMA API."""

from typing import Any

from .client import ImaClient


class TagsAPI:
    """Tag management operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def get_tags(self, **kwargs) -> dict[str, Any]:
        """Get all tags for the current user."""
        return self.client.post("knowledge/get_tags", kwargs or {})

    def update_tags(
        self, knowledge_id: str, tags: list[str], **kwargs
    ) -> dict[str, Any]:
        """Update tags for a knowledge item."""
        payload: dict[str, Any] = {"knowledge_id": knowledge_id, "tags": tags}
        payload.update(kwargs)
        return self.client.post("knowledge/update_tags", payload)

    def search_tags(self, keyword: str, **kwargs) -> dict[str, Any]:
        """Search tags by keyword."""
        payload: dict[str, Any] = {"keyword": keyword}
        payload.update(kwargs)
        return self.client.post("knowledge/search_tags", payload)

    def rename_tag(self, old_name: str, new_name: str, **kwargs) -> dict[str, Any]:
        """Rename a tag."""
        payload: dict[str, Any] = {"old_name": old_name, "new_name": new_name}
        payload.update(kwargs)
        return self.client.post("knowledge/rename_tag", payload)

    def del_tags(self, tags: list[str], **kwargs) -> dict[str, Any]:
        """Delete tags."""
        payload: dict[str, Any] = {"tags": tags}
        payload.update(kwargs)
        return self.client.post("knowledge/del_tags", payload)

    def batch_update_tags(
        self, knowledge_ids: list[str], tags: list[str], **kwargs
    ) -> dict[str, Any]:
        """Batch update tags for multiple knowledge items."""
        payload: dict[str, Any] = {"knowledge_ids": knowledge_ids, "tags": tags}
        payload.update(kwargs)
        return self.client.post("knowledge/batch_update_tags", payload)

    def get_tag_view(self, **kwargs) -> dict[str, Any]:
        """Get tag view (organized by tag)."""
        return self.client.post("knowledge/get_tag_view", kwargs or {})
