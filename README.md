# IMA知识库 MCP Server

基于 [Model Context Protocol](https://modelcontextprotocol.io/) 的 IMA知识库 本地服务，支持通过 CLI 工具（Cortex Code、Cline、Continue 等）调用 IMA 知识库的全部功能。

## 功能

- 知识管理 CRUD（添加/获取/删除/列表/重命名/复制/替换）
- 知识库管理（创建/删除/更新/列表/搜索）
- 网页内容提取（URL解析/批量导入）
- 标签管理（获取/更新/搜索/重命名/删除/批量更新）
- 搜索功能（全文搜索/搜索建议/URL存在检测）
- 文件上传（媒体注册/上传凭证/管理）
- AI摘要 & 关键要点

## 安装

```bash
cd ima-mcp
uv sync
```

## 配置认证

1. 复制 `config.json.example` 为 `config.json`：
```bash
cp config.json.example config.json
```

2. 填入你的 IMA 认证信息（从浏览器开发者工具中获取）：
```json
{
  "user_id": "你的用户ID",
  "token": "你的IMA-TOKEN",
  "refresh_token": "你的IMA-REFRESH-TOKEN"
}
```

### 如何获取 Token

1. 打开浏览器访问 https://ima.qq.com
2. 登录你的账号
3. 打开开发者工具 (F12) → Network 面板
4. 刷新页面，找到任意 `cgi-bin/` 请求
5. 查看请求头中的 `x-ima-cookie`，从中提取：
   - `IMA-UID` → 对应 `user_id`
   - `IMA-TOKEN` → 对应 `token`
   - `IMA-REFRESH-TOKEN` → 对应 `refresh_token`

### 认证机制

本项目使用 IMA 的 cookie-based 认证：
- 请求头 `x-ima-cookie` 包含完整元数据（PLATFORM、CLIENT-TYPE、UID-TYPE 等）及 token
- 请求头 `x-ima-bkn` 包含 token 的哈希值
- Token 过期时会自动使用 `refresh_token` 刷新，刷新后自动保存到 `config.json`

> **注意：** `.env` 中的 `Client_ID` / `API_Key` 是 IMA Open API 的凭证，但该功能目前尚未在服务端实现。当前仅支持 cookie-based 认证。

## 运行

```bash
# 直接运行（stdio模式）
uv run python ima_mcp_server.py
```

## 配置到 CLI 工具

### Cortex Code (Snowflake)

编辑 `~/.snowflake/cortex/mcp.json`：
```json
{
  "mcpServers": {
    "ima-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "C:/Users/heda/Downloads/ima-skill/ima-mcp", "run", "python", "ima_mcp_server.py"]
    }
  }
}
```

### Cline / Continue / 其他

```json
{
  "ima-mcp": {
    "command": "uv",
    "args": ["--directory", "/path/to/ima-mcp", "run", "python", "ima_mcp_server.py"]
  }
}
```

## 可用 Tools

| 工具名 | 功能 |
|--------|------|
| `ima_auth_status` | 检查认证状态 |
| `ima_refresh_token` | 刷新token |
| `ima_add_knowledge` | 添加知识条目 |
| `ima_get_knowledge` | 获取知识详情 |
| `ima_del_knowledge` | 删除知识条目 |
| `ima_get_knowledge_list` | 获取知识列表 |
| `ima_rename_knowledge` | 重命名知识 |
| `ima_copy_knowledge` | 复制知识 |
| `ima_replace_knowledge` | 更新知识内容 |
| `ima_set_knowledge_top` | 置顶知识 |
| `ima_get_knowledge_summary` | AI摘要 |
| `ima_get_key_points` | 关键要点 |
| `ima_get_knowledge_base_list` | 知识库列表 |
| `ima_get_knowledge_base` | 知识库详情 |
| `ima_create_knowledge_base` | 创建知识库 |
| `ima_delete_knowledge_base` | 删除知识库 |
| `ima_update_knowledge_base_info` | 更新知识库 |
| `ima_get_user_space` | 用户空间 |
| `ima_get_folder_list` | 文件夹列表 |
| `ima_create_folder` | 创建文件夹 |
| `ima_import_notes` | 导入笔记 |
| `ima_get_home_page_data` | 首页数据 |
| `ima_search_knowledge` | 搜索知识 |
| `ima_get_knowledge_sug` | 搜索建议 |
| `ima_is_knowledge_exist` | URL存在检测 |
| `ima_search_knowledge_base` | 搜索知识库 |
| `ima_get_tags` | 获取标签 |
| `ima_update_tags` | 更新标签 |
| `ima_search_tags` | 搜索标签 |
| `ima_rename_tag` | 重命名标签 |
| `ima_del_tags` | 删除标签 |
| `ima_batch_update_tags` | 批量更新标签 |
| `ima_get_tag_view` | 标签视图 |
| `ima_parse_knowledge` | 网页内容提取 |
| `ima_check_link` | 检查URL |
| `ima_import_urls` | 批量导入URL |
| `ima_create_media` | 创建媒体 |
| `ima_get_upload_credential` | 上传凭证 |
| `ima_get_media` | 获取媒体 |
| `ima_delete_temp_media` | 删除临时媒体 |

## 技术栈

- Python 3.11+
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [httpx](https://www.python-httpx.org/) - HTTP client
- [uv](https://github.com/astral-sh/uv) - Package manager
