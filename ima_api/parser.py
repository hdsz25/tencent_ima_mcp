"""Web content extraction/parsing for IMA API."""

from typing import Any

from .client import ImaClient


class ParserAPI:
    """Web content extraction and parsing operations."""

    def __init__(self, client: ImaClient):
        self.client = client

    def parse_knowledge(self, url: str, **kwargs) -> dict[str, Any]:
        """
        Parse/extract content from a URL.

        This uses IMA's server-side parser to extract the main content
        from a web page, similar to reader mode.

        Args:
            url: The URL to parse/extract content from
        """
        payload: dict[str, Any] = {"url": url}
        payload.update(kwargs)
        return self.client.post("knowledge/parse_knowledge", payload)

    def check_link(self, url: str, **kwargs) -> dict[str, Any]:
        """
        Check if a URL is valid and accessible.

        Args:
            url: The URL to check
        """
        payload: dict[str, Any] = {"url": url}
        payload.update(kwargs)
        return self.client.post("knowledge/check_link", payload)

    def import_urls(
        self, knowledge_base_id: str, urls: list[str], **kwargs
    ) -> dict[str, Any]:
        """
        Import multiple URLs into a knowledge base (batch parse and save).

        Args:
            knowledge_base_id: Target knowledge base ID
            urls: List of URLs to import
        """
        payload: dict[str, Any] = {
            "knowledge_base_id": knowledge_base_id,
            "urls": urls,
        }
        payload.update(kwargs)
        return self.client.post("knowledge_base/import_urls", payload)
