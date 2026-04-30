"""Knowledge CRUD operations for IMA API."""

from typing import Any

from .client import ImaClient


class KnowledgeAPI:
    """Knowledge item CRUD operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def add_knowledge(
        self,
        title: str,
        content: str,
        source_url: str = "",
        knowledge_type: int = 1,
        tags: list[str] | None = None,
        knowledge_base_id: str = "",
        **kwargs,
    ) -> dict[str, Any]:
        """
        Add a new knowledge item.

        Args:
            title: Knowledge title
            content: Knowledge content (HTML or text)
            source_url: Original URL source
            knowledge_type: Type of knowledge (1=note, 2=web, 3=file, etc.)
            tags: Optional list of tag names
            knowledge_base_id: Optional knowledge base to add to
            **kwargs: Additional fields to include in the request
        """
        payload: dict[str, Any] = {
            "title": title,
            "content": content,
            "knowledge_type": knowledge_type,
        }
        if source_url:
            payload["source_url"] = source_url
        if tags:
            payload["tags"] = tags
        if knowledge_base_id:
            payload["knowledge_base_id"] = knowledge_base_id
        payload.update(kwargs)
        return self.client.post("knowledge/add_knowledge", payload)

    def get_knowledge(self, knowledge_id: str) -> dict[str, Any]:
        """Get a single knowledge item by ID."""
        return self.client.post("knowledge/get_knowledge", {"knowledge_id": knowledge_id})

    def del_knowledge(self, knowledge_id: str) -> dict[str, Any]:
        """Delete a knowledge item."""
        return self.client.post("knowledge/del_knowledge", {"knowledge_id": knowledge_id})

    def get_knowledge_list(
        self,
        page: int = 1,
        page_size: int = 20,
        knowledge_base_id: str = "",
        folder_id: str = "",
        sort_type: int = 0,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Get paginated list of knowledge items.

        Args:
            page: Page number (1-based)
            page_size: Items per page
            knowledge_base_id: Filter by knowledge base
            folder_id: Filter by folder
            sort_type: Sort order (0=newest first, 1=oldest first)
        """
        payload: dict[str, Any] = {
            "page": page,
            "page_size": page_size,
            "sort_type": sort_type,
        }
        if knowledge_base_id:
            payload["knowledge_base_id"] = knowledge_base_id
        if folder_id:
            payload["folder_id"] = folder_id
        payload.update(kwargs)
        return self.client.post("knowledge/get_knowledge_list", payload)

    def rename_knowledge(self, knowledge_id: str, title: str) -> dict[str, Any]:
        """Rename a knowledge item."""
        return self.client.post(
            "knowledge/rename_knowledge",
            {"knowledge_id": knowledge_id, "title": title},
        )

    def copy_knowledge(
        self, knowledge_id: str, knowledge_base_id: str = ""
    ) -> dict[str, Any]:
        """Copy a knowledge item, optionally to another knowledge base."""
        payload: dict[str, Any] = {"knowledge_id": knowledge_id}
        if knowledge_base_id:
            payload["knowledge_base_id"] = knowledge_base_id
        return self.client.post("knowledge/copy_knowledge", payload)

    def replace_knowledge(
        self, knowledge_id: str, content: str, title: str = "", **kwargs
    ) -> dict[str, Any]:
        """Replace/update a knowledge item's content."""
        payload: dict[str, Any] = {"knowledge_id": knowledge_id, "content": content}
        if title:
            payload["title"] = title
        payload.update(kwargs)
        return self.client.post("knowledge/replace_knowledge", payload)

    def is_knowledge_exist(self, source_url: str) -> dict[str, Any]:
        """Check if knowledge with given URL already exists."""
        return self.client.post(
            "knowledge/is_knowledge_exist", {"source_url": source_url}
        )

    def report_knowledge(self, knowledge_id: str, **kwargs) -> dict[str, Any]:
        """Report/flag a knowledge item."""
        payload: dict[str, Any] = {"knowledge_id": knowledge_id}
        payload.update(kwargs)
        return self.client.post("knowledge/report_knowledge", payload)

    def set_knowledge_top(
        self, knowledge_id: str, is_top: bool = True
    ) -> dict[str, Any]:
        """Pin/unpin a knowledge item to top."""
        return self.client.post(
            "knowledge/set_knowledge_top",
            {"knowledge_id": knowledge_id, "is_top": is_top},
        )

    def update_knowledge_access_status(
        self, knowledge_id: str, access_status: int = 0
    ) -> dict[str, Any]:
        """Update the access status of a knowledge item."""
        return self.client.post(
            "knowledge/update_knowledge_access_status",
            {"knowledge_id": knowledge_id, "access_status": access_status},
        )

    def get_knowledge_summary(self, knowledge_id: str) -> dict[str, Any]:
        """Get AI-generated summary of a knowledge item."""
        return self.client.post(
            "knowledge/get_knowledge_summary", {"knowledge_id": knowledge_id}
        )

    def get_key_points(self, knowledge_id: str) -> dict[str, Any]:
        """Get key points extracted from a knowledge item."""
        return self.client.post(
            "knowledge/get_key_points", {"knowledge_id": knowledge_id}
        )

    def get_key_point(self, knowledge_id: str, key_point_id: str) -> dict[str, Any]:
        """Get a specific key point."""
        return self.client.post(
            "knowledge/get_key_point",
            {"knowledge_id": knowledge_id, "key_point_id": key_point_id},
        )
