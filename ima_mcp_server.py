"""IMA知识库 MCP Server - 本地运行供CLI工具调用。"""

import json
import os
import sys

from fastmcp import FastMCP

# Ensure working directory is the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from ima_api.client import ImaClient
from ima_api.auth import AuthManager
from ima_api.knowledge import KnowledgeAPI
from ima_api.tags import TagsAPI
from ima_api.search import SearchAPI

# Initialize MCP server
mcp = FastMCP("IMA知识库 MCP Server")

# Initialize API client and modules
client = ImaClient()
auth = AuthManager(client)
knowledge_api = KnowledgeAPI(client)
tags_api = TagsAPI(client)
search_api = SearchAPI(client)


def _format_response(data: dict) -> str:
    """Format API response as JSON string."""
    return json.dumps(data, ensure_ascii=False, indent=2)


# ============================================================
# Auth Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_auth_status() -> str:
    """检查IMA知识库认证状态，返回当前用户ID和token是否有效。"""
    info = auth.get_user_info()
    return _format_response(info)


@mcp.tool(output_schema=None)
def ima_refresh_token() -> str:
    """手动刷新IMA知识库的access token。"""
    success = auth.refresh()
    return _format_response({"success": success})


# ============================================================
# Knowledge Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_get_knowledge_list(
    limit: int = 20,
    offset: int = 0,
    sort_type: int = 0,
) -> str:
    """
    获取知识条目列表（分页）。

    Args:
        limit: 返回条目数量上限
        offset: 跳过的条目数量
        sort_type: 排序方式 (0=最新优先, 1=最旧优先)
    """
    result = knowledge_api.get_knowledge_list(
        limit=limit,
        offset=offset,
        sort_type=sort_type,
    )
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_knowledge(media_id: str) -> str:
    """
    获取指定ID的知识条目详情。

    Args:
        media_id: 知识条目的media_id
    """
    result = knowledge_api.get_knowledge(media_id)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_del_knowledge(media_id: str) -> str:
    """
    删除指定的知识条目。

    Args:
        media_id: 要删除的知识条目media_id
    """
    result = knowledge_api.del_knowledge(media_id)
    return _format_response(result)


# ============================================================
# Search Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_search_knowledge(keyword: str, limit: int = 20) -> str:
    """
    搜索知识条目。

    Args:
        keyword: 搜索关键词
        limit: 返回结果数量上限
    """
    result = search_api.search_knowledge(keyword=keyword, limit=limit)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_knowledge_sug(keyword: str) -> str:
    """
    获取搜索建议。

    Args:
        keyword: 搜索关键词
    """
    result = search_api.get_knowledge_sug(keyword)
    return _format_response(result)


# ============================================================
# Tag Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_get_tags(limit: int = 50) -> str:
    """
    获取所有标签列表。

    Args:
        limit: 返回标签数量上限
    """
    result = tags_api.get_tags(limit=limit)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_update_tags(media_id: str, tags: str) -> str:
    """
    更新知识条目的标签。

    Args:
        media_id: 知识条目的media_id
        tags: 标签列表，用逗号分隔
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    result = tags_api.update_tags(media_id, tag_list)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_search_tags(keyword: str, limit: int = 20) -> str:
    """
    搜索标签。

    Args:
        keyword: 搜索关键词
        limit: 返回结果数量上限
    """
    result = tags_api.search_tags(keyword, limit=limit)
    return _format_response(result)


if __name__ == "__main__":
    mcp.run("stdio")
