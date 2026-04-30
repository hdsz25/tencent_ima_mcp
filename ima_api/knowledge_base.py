"""Knowledge Base management operations for IMA API."""

from typing import Any

from .client import ImaClient


class KnowledgeBaseAPI:
    """Knowledge base management operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def get_knowledge_base_list(
        self, page: int = 1, page_size: int = 20, **kwargs
    ) -> dict[str, Any]:
        """Get list of knowledge bases."""
        payload: dict[str, Any] = {"page": page, "page_size": page_size}
        payload.update(kwargs)
        return self.client.post("knowledge_base/get_knowledge_base_list", payload)

    def get_knowledge_base(self, knowledge_base_id: str) -> dict[str, Any]:
        """Get details of a specific knowledge base."""
        return self.client.post(
            "knowledge_base/get_knowledge_base",
            {"knowledge_base_id": knowledge_base_id},
        )

    def create_knowledge_base(
        self, name: str, description: str = "", **kwargs
    ) -> dict[str, Any]:
        """
        Create a new knowledge base.

        Args:
            name: Knowledge base name
            description: Optional description
        """
        payload: dict[str, Any] = {"name": name}
        if description:
            payload["description"] = description
        payload.update(kwargs)
        return self.client.post("knowledge_base/create_knowledge_base", payload)

    def delete_knowledge_base(self, knowledge_base_id: str) -> dict[str, Any]:
        """Delete a knowledge base."""
        return self.client.post(
            "knowledge_base/delete_knowledge_base",
            {"knowledge_base_id": knowledge_base_id},
        )

    def update_basic_info(
        self, knowledge_base_id: str, name: str = "", description: str = "", **kwargs
    ) -> dict[str, Any]:
        """Update knowledge base basic info (name, description)."""
        payload: dict[str, Any] = {"knowledge_base_id": knowledge_base_id}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        payload.update(kwargs)
        return self.client.post("knowledge_base/update_basic_info", payload)

    def update_permission_info(
        self, knowledge_base_id: str, **kwargs
    ) -> dict[str, Any]:
        """Update knowledge base permission settings."""
        payload: dict[str, Any] = {"knowledge_base_id": knowledge_base_id}
        payload.update(kwargs)
        return self.client.post("knowledge_base/update_permission_info", payload)

    def get_addable_knowledge_base_list(self, **kwargs) -> dict[str, Any]:
        """Get list of knowledge bases that can be added to."""
        return self.client.post(
            "knowledge_base/get_addable_knowledge_base_list", kwargs or {}
        )

    def batch_get_note_addable_knowledge_base_list(
        self, knowledge_ids: list[str], **kwargs
    ) -> dict[str, Any]:
        """Get addable knowledge bases for multiple notes."""
        payload: dict[str, Any] = {"knowledge_ids": knowledge_ids}
        payload.update(kwargs)
        return self.client.post(
            "knowledge_base/batch_get_note_addable_knowledge_base_list", payload
        )

    def check_repeated_names(self, name: str, **kwargs) -> dict[str, Any]:
        """Check if a knowledge base name is already taken."""
        payload: dict[str, Any] = {"name": name}
        payload.update(kwargs)
        return self.client.post("knowledge_base/check_repeated_names", payload)

    def search_knowledge_base(self, keyword: str, **kwargs) -> dict[str, Any]:
        """Search for knowledge bases by keyword."""
        payload: dict[str, Any] = {"keyword": keyword}
        payload.update(kwargs)
        return self.client.post("knowledge_base/search_knowledge_base", payload)

    def check_content_status_in_knowledge_base(
        self, knowledge_base_id: str, source_url: str = "", **kwargs
    ) -> dict[str, Any]:
        """Check if content already exists in a knowledge base."""
        payload: dict[str, Any] = {"knowledge_base_id": knowledge_base_id}
        if source_url:
            payload["source_url"] = source_url
        payload.update(kwargs)
        return self.client.post(
            "knowledge_base/check_content_status_in_knowledge_base", payload
        )

    def batch_check_note_status_in_knowledge_base(
        self, knowledge_base_id: str, knowledge_ids: list[str], **kwargs
    ) -> dict[str, Any]:
        """Batch check status of notes in a knowledge base."""
        payload: dict[str, Any] = {
            "knowledge_base_id": knowledge_base_id,
            "knowledge_ids": knowledge_ids,
        }
        payload.update(kwargs)
        return self.client.post(
            "knowledge_base/batch_check_note_status_in_knowledge_base", payload
        )

    def get_knowledge_base_count(self, **kwargs) -> dict[str, Any]:
        """Get total count of knowledge bases."""
        return self.client.post("knowledge_base/get_knowledge_base_count", kwargs or {})

    def pre_check_import(
        self, knowledge_base_id: str, **kwargs
    ) -> dict[str, Any]:
        """Pre-check before importing to knowledge base."""
        payload: dict[str, Any] = {"knowledge_base_id": knowledge_base_id}
        payload.update(kwargs)
        return self.client.post("knowledge_base/pre_check_import", payload)

    def get_user_space(self, **kwargs) -> dict[str, Any]:
        """Get user's personal space info."""
        return self.client.post("knowledge_base/get_user_space", kwargs or {})

    def get_folder_list(
        self, knowledge_base_id: str = "", parent_id: str = "", **kwargs
    ) -> dict[str, Any]:
        """Get list of folders in a knowledge base."""
        payload: dict[str, Any] = {}
        if knowledge_base_id:
            payload["knowledge_base_id"] = knowledge_base_id
        if parent_id:
            payload["parent_id"] = parent_id
        payload.update(kwargs)
        return self.client.post("knowledge_base/get_folder_list", payload)

    def create_folder(
        self, name: str, knowledge_base_id: str = "", parent_id: str = "", **kwargs
    ) -> dict[str, Any]:
        """Create a new folder in a knowledge base."""
        payload: dict[str, Any] = {"name": name}
        if knowledge_base_id:
            payload["knowledge_base_id"] = knowledge_base_id
        if parent_id:
            payload["parent_id"] = parent_id
        payload.update(kwargs)
        return self.client.post("knowledge_base/create_folder", payload)

    def import_notes(
        self, knowledge_base_id: str, knowledge_ids: list[str], **kwargs
    ) -> dict[str, Any]:
        """Import notes into a knowledge base."""
        payload: dict[str, Any] = {
            "knowledge_base_id": knowledge_base_id,
            "knowledge_ids": knowledge_ids,
        }
        payload.update(kwargs)
        return self.client.post("knowledge_base/import_notes", payload)

    def import_urls(
        self, knowledge_base_id: str, urls: list[str], **kwargs
    ) -> dict[str, Any]:
        """Import URLs into a knowledge base."""
        payload: dict[str, Any] = {
            "knowledge_base_id": knowledge_base_id,
            "urls": urls,
        }
        payload.update(kwargs)
        return self.client.post("knowledge_base/import_urls", payload)

    def set_knowledge_base_top(
        self, knowledge_base_id: str, is_top: bool = True
    ) -> dict[str, Any]:
        """Pin/unpin a knowledge base to top."""
        return self.client.post(
            "knowledge_base/set_knowledge_base_top",
            {"knowledge_base_id": knowledge_base_id, "is_top": is_top},
        )

    def cancel_cross_kb_op(self, **kwargs) -> dict[str, Any]:
        """Cancel a cross knowledge base operation."""
        return self.client.post("knowledge_base/cancel_cross_kb_op", kwargs or {})

    def get_home_page_data(self, **kwargs) -> dict[str, Any]:
        """Get home page data (recent items, stats)."""
        return self.client.post("knowledge_base/get_home_page_data", kwargs or {})

    def get_config(self, **kwargs) -> dict[str, Any]:
        """Get server-side configuration."""
        return self.client.post("knowledge_base/get_config", kwargs or {})
