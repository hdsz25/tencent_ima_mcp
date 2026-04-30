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
from ima_api.knowledge_base import KnowledgeBaseAPI
from ima_api.tags import TagsAPI
from ima_api.search import SearchAPI
from ima_api.media import MediaAPI
from ima_api.parser import ParserAPI

# Initialize MCP server
mcp = FastMCP("IMA知识库 MCP Server")

# Initialize API client and modules
client = ImaClient()
auth = AuthManager(client)
knowledge_api = KnowledgeAPI(client)
kb_api = KnowledgeBaseAPI(client)
tags_api = TagsAPI(client)
search_api = SearchAPI(client)
media_api = MediaAPI(client)
parser_api = ParserAPI(client)


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
# Knowledge CRUD Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_add_knowledge(
    title: str,
    content: str,
    source_url: str = "",
    knowledge_type: int = 1,
    tags: str = "",
    knowledge_base_id: str = "",
) -> str:
    """
    添加新的知识条目到IMA知识库。

    Args:
        title: 知识标题
        content: 知识内容（支持HTML或纯文本）
        source_url: 来源URL（可选）
        knowledge_type: 知识类型 (1=笔记, 2=网页, 3=文件)
        tags: 标签列表，用逗号分隔（可选）
        knowledge_base_id: 目标知识库ID（可选）
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else None
    result = knowledge_api.add_knowledge(
        title=title,
        content=content,
        source_url=source_url,
        knowledge_type=knowledge_type,
        tags=tag_list,
        knowledge_base_id=knowledge_base_id,
    )
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_knowledge(knowledge_id: str) -> str:
    """
    获取指定ID的知识条目详情。

    Args:
        knowledge_id: 知识条目ID
    """
    result = knowledge_api.get_knowledge(knowledge_id)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_del_knowledge(knowledge_id: str) -> str:
    """
    删除指定的知识条目。

    Args:
        knowledge_id: 要删除的知识条目ID
    """
    result = knowledge_api.del_knowledge(knowledge_id)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_knowledge_list(
    page: int = 1,
    page_size: int = 20,
    knowledge_base_id: str = "",
    folder_id: str = "",
    sort_type: int = 0,
) -> str:
    """
    获取知识条目列表（分页）。

    Args:
        page: 页码（从1开始）
        page_size: 每页数量
        knowledge_base_id: 按知识库过滤（可选）
        folder_id: 按文件夹过滤（可选）
        sort_type: 排序方式 (0=最新优先, 1=最旧优先)
    """
    result = knowledge_api.get_knowledge_list(
        page=page,
        page_size=page_size,
        knowledge_base_id=knowledge_base_id,
        folder_id=folder_id,
        sort_type=sort_type,
    )
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_rename_knowledge(knowledge_id: str, title: str) -> str:
    """
    重命名知识条目。

    Args:
        knowledge_id: 知识条目ID
        title: 新标题
    """
    result = knowledge_api.rename_knowledge(knowledge_id, title)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_copy_knowledge(knowledge_id: str, knowledge_base_id: str = "") -> str:
    """
    复制知识条目到另一个知识库。

    Args:
        knowledge_id: 源知识条目ID
        knowledge_base_id: 目标知识库ID（可选）
    """
    result = knowledge_api.copy_knowledge(knowledge_id, knowledge_base_id)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_replace_knowledge(knowledge_id: str, content: str, title: str = "") -> str:
    """
    替换/更新知识条目的内容。

    Args:
        knowledge_id: 知识条目ID
        content: 新内容
        title: 新标题（可选）
    """
    result = knowledge_api.replace_knowledge(knowledge_id, content, title)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_set_knowledge_top(knowledge_id: str, is_top: bool = True) -> str:
    """
    置顶/取消置顶知识条目。

    Args:
        knowledge_id: 知识条目ID
        is_top: True=置顶, False=取消置顶
    """
    result = knowledge_api.set_knowledge_top(knowledge_id, is_top)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_knowledge_summary(knowledge_id: str) -> str:
    """
    获取知识条目的AI摘要。

    Args:
        knowledge_id: 知识条目ID
    """
    result = knowledge_api.get_knowledge_summary(knowledge_id)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_key_points(knowledge_id: str) -> str:
    """
    获取知识条目的关键要点。

    Args:
        knowledge_id: 知识条目ID
    """
    result = knowledge_api.get_key_points(knowledge_id)
    return _format_response(result)


# ============================================================
# Knowledge Base Management Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_get_knowledge_base_list(page: int = 1, page_size: int = 20) -> str:
    """
    获取知识库列表。

    Args:
        page: 页码
        page_size: 每页数量
    """
    result = kb_api.get_knowledge_base_list(page=page, page_size=page_size)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_knowledge_base(knowledge_base_id: str) -> str:
    """
    获取指定知识库的详细信息。

    Args:
        knowledge_base_id: 知识库ID
    """
    result = kb_api.get_knowledge_base(knowledge_base_id)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_create_knowledge_base(name: str, description: str = "") -> str:
    """
    创建新的知识库。

    Args:
        name: 知识库名称
        description: 知识库描述（可选）
    """
    result = kb_api.create_knowledge_base(name=name, description=description)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_delete_knowledge_base(knowledge_base_id: str) -> str:
    """
    删除知识库。

    Args:
        knowledge_base_id: 要删除的知识库ID
    """
    result = kb_api.delete_knowledge_base(knowledge_base_id)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_update_knowledge_base_info(
    knowledge_base_id: str, name: str = "", description: str = ""
) -> str:
    """
    更新知识库基本信息。

    Args:
        knowledge_base_id: 知识库ID
        name: 新名称（可选）
        description: 新描述（可选）
    """
    result = kb_api.update_basic_info(
        knowledge_base_id=knowledge_base_id, name=name, description=description
    )
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_user_space() -> str:
    """获取用户个人空间信息。"""
    result = kb_api.get_user_space()
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_folder_list(knowledge_base_id: str = "", parent_id: str = "") -> str:
    """
    获取知识库中的文件夹列表。

    Args:
        knowledge_base_id: 知识库ID（可选）
        parent_id: 父文件夹ID（可选）
    """
    result = kb_api.get_folder_list(
        knowledge_base_id=knowledge_base_id, parent_id=parent_id
    )
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_create_folder(
    name: str, knowledge_base_id: str = "", parent_id: str = ""
) -> str:
    """
    在知识库中创建文件夹。

    Args:
        name: 文件夹名称
        knowledge_base_id: 知识库ID（可选）
        parent_id: 父文件夹ID（可选）
    """
    result = kb_api.create_folder(
        name=name, knowledge_base_id=knowledge_base_id, parent_id=parent_id
    )
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_import_notes(knowledge_base_id: str, knowledge_ids: str) -> str:
    """
    将笔记导入到知识库。

    Args:
        knowledge_base_id: 目标知识库ID
        knowledge_ids: 知识条目ID列表，用逗号分隔
    """
    ids = [i.strip() for i in knowledge_ids.split(",") if i.strip()]
    result = kb_api.import_notes(knowledge_base_id=knowledge_base_id, knowledge_ids=ids)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_home_page_data() -> str:
    """获取首页数据（最近条目、统计等）。"""
    result = kb_api.get_home_page_data()
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_set_knowledge_base_top(knowledge_base_id: str, is_top: bool = True) -> str:
    """
    置顶/取消置顶知识库。

    Args:
        knowledge_base_id: 知识库ID
        is_top: True=置顶, False=取消置顶
    """
    result = kb_api.set_knowledge_base_top(knowledge_base_id, is_top)
    return _format_response(result)


# ============================================================
# Search Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_search_knowledge(
    keyword: str,
    page: int = 1,
    page_size: int = 20,
    knowledge_base_id: str = "",
) -> str:
    """
    搜索知识条目。

    Args:
        keyword: 搜索关键词
        page: 页码
        page_size: 每页数量
        knowledge_base_id: 限定在某个知识库内搜索（可选）
    """
    result = search_api.search_knowledge(
        keyword=keyword,
        page=page,
        page_size=page_size,
        knowledge_base_id=knowledge_base_id,
    )
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


@mcp.tool(output_schema=None)
def ima_is_knowledge_exist(source_url: str) -> str:
    """
    检查指定URL的内容是否已存在于知识库中。

    Args:
        source_url: 要检查的URL
    """
    result = search_api.is_knowledge_exist(source_url)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_search_knowledge_base(keyword: str) -> str:
    """
    搜索知识库。

    Args:
        keyword: 搜索关键词
    """
    result = kb_api.search_knowledge_base(keyword)
    return _format_response(result)


# ============================================================
# Tag Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_get_tags() -> str:
    """获取所有标签列表。"""
    result = tags_api.get_tags()
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_update_tags(knowledge_id: str, tags: str) -> str:
    """
    更新知识条目的标签。

    Args:
        knowledge_id: 知识条目ID
        tags: 标签列表，用逗号分隔
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    result = tags_api.update_tags(knowledge_id, tag_list)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_search_tags(keyword: str) -> str:
    """
    搜索标签。

    Args:
        keyword: 搜索关键词
    """
    result = tags_api.search_tags(keyword)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_rename_tag(old_name: str, new_name: str) -> str:
    """
    重命名标签。

    Args:
        old_name: 原标签名
        new_name: 新标签名
    """
    result = tags_api.rename_tag(old_name, new_name)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_del_tags(tags: str) -> str:
    """
    删除标签。

    Args:
        tags: 要删除的标签列表，用逗号分隔
    """
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    result = tags_api.del_tags(tag_list)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_batch_update_tags(knowledge_ids: str, tags: str) -> str:
    """
    批量更新多个知识条目的标签。

    Args:
        knowledge_ids: 知识条目ID列表，用逗号分隔
        tags: 标签列表，用逗号分隔
    """
    ids = [i.strip() for i in knowledge_ids.split(",") if i.strip()]
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    result = tags_api.batch_update_tags(ids, tag_list)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_tag_view() -> str:
    """获取标签视图（按标签分组的知识条目）。"""
    result = tags_api.get_tag_view()
    return _format_response(result)


# ============================================================
# Web Content Extraction Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_parse_knowledge(url: str) -> str:
    """
    从URL提取网页正文内容（类似阅读模式）。

    使用IMA服务端解析器提取网页的主要内容。

    Args:
        url: 要解析的网页URL
    """
    result = parser_api.parse_knowledge(url)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_check_link(url: str) -> str:
    """
    检查URL是否有效可访问。

    Args:
        url: 要检查的URL
    """
    result = parser_api.check_link(url)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_import_urls(knowledge_base_id: str, urls: str) -> str:
    """
    批量导入URL到知识库（解析并保存网页内容）。

    Args:
        knowledge_base_id: 目标知识库ID
        urls: URL列表，用逗号分隔
    """
    url_list = [u.strip() for u in urls.split(",") if u.strip()]
    result = parser_api.import_urls(knowledge_base_id, url_list)
    return _format_response(result)


# ============================================================
# Media/File Upload Tools
# ============================================================


@mcp.tool(output_schema=None)
def ima_create_media(file_name: str, file_size: int, file_type: str = "") -> str:
    """
    创建媒体条目（上传前注册）。

    Args:
        file_name: 文件名
        file_size: 文件大小（字节）
        file_type: 文件MIME类型（可选）
    """
    result = media_api.create_media(file_name, file_size, file_type)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_upload_credential() -> str:
    """获取文件上传凭证（用于直传）。"""
    result = media_api.get_upload_credential()
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_get_media(media_id: str) -> str:
    """
    获取媒体文件详情。

    Args:
        media_id: 媒体文件ID
    """
    result = media_api.get_media(media_id)
    return _format_response(result)


@mcp.tool(output_schema=None)
def ima_delete_temp_media(media_id: str) -> str:
    """
    删除临时媒体文件。

    Args:
        media_id: 媒体文件ID
    """
    result = media_api.delete_temp_media(media_id)
    return _format_response(result)


if __name__ == "__main__":
    mcp.run("stdio")
