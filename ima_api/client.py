"""IMA API HTTP Client with cookie-based authentication."""

import json
import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


BASE_URL = "https://ima.qq.com/cgi-bin/"


def _bkn_hash(token: str) -> int:
    """Compute the BKN hash of an IMA token (same as extension's Hm function)."""
    h = 5381
    for c in token:
        h += (h << 5) + ord(c)
    return h & 0x7FFFFFFF


class ImaClient:
    """HTTP client for IMA知识库 API using cookie-based auth.

    Authentication uses the same mechanism as the Chrome extension:
    - x-ima-cookie header with IMA-TOKEN
    - x-ima-bkn header with hash of the token
    - Token refresh via auth_login/refresh endpoint

    Configuration is loaded from .env (Client_ID, API_Key) or config.json
    (user_id, token, refresh_token).
    """

    def __init__(self):
        self._project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        load_dotenv(os.path.join(self._project_root, ".env"))
        self._load_config()
        self._client = httpx.Client(timeout=30.0)

    def _load_config(self):
        """Load credentials from .env or config.json."""
        # Try .env first (Client_ID + API_Key)
        self.client_id = os.getenv("Client_ID", "")
        self.api_key = os.getenv("API_Key", "")

        # Load config.json for user session tokens
        config_path = Path(self._project_root) / "config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.user_id = config.get("user_id", "")
            self.token = config.get("token", "")
            self.refresh_token = config.get("refresh_token", "")
        else:
            self.user_id = ""
            self.token = ""
            self.refresh_token = ""

    def _save_config(self):
        """Save current session tokens to config.json."""
        config_path = Path(self._project_root) / "config.json"
        config = {}
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        config["user_id"] = self.user_id
        config["token"] = self.token
        config["refresh_token"] = self.refresh_token
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def _get_headers(self) -> dict:
        """Build request headers with IMA authentication."""
        headers = {"Content-Type": "application/json"}

        if self.token:
            # Build full x-ima-cookie with required metadata fields
            cookie_parts = [
                "PLATFORM=H5",
                "CLIENT-TYPE=256053",
                "WEB-VERSION=999.999.999",
                f"IMA-UID={self.user_id}" if self.user_id else "",
                f"IMA-TOKEN={self.token}",
                f"IMA-REFRESH-TOKEN={self.refresh_token}" if self.refresh_token else "",
                "UID-TYPE=2",
                "TOKEN-TYPE=14",
            ]
            headers["x-ima-cookie"] = "; ".join(p for p in cookie_parts if p)
            headers["x-ima-bkn"] = str(_bkn_hash(self.token))
            headers["from_browser_ima"] = "1"

        return headers

    def _try_refresh_token(self) -> bool:
        """Refresh the access token using refresh_token."""
        if not self.user_id or not self.refresh_token:
            return False
        try:
            resp = self._client.post(
                f"{BASE_URL}auth_login/refresh",
                json={
                    "user_id": self.user_id,
                    "refresh_token": self.refresh_token,
                },
                headers={"Content-Type": "application/json"},
            )
            if resp.status_code != 200:
                return False
            data = resp.json()
            if data.get("code") != 0:
                return False
            result = data.get("data", data)
            new_token = result.get("token", "")
            new_refresh = result.get("refresh_token", "")
            new_user_id = result.get("user_id", self.user_id)
            if new_token:
                self.token = new_token
            if new_refresh:
                self.refresh_token = new_refresh
            if new_user_id:
                self.user_id = new_user_id
            self._save_config()
            return True
        except Exception:
            return False

    def post(self, endpoint: str, payload: dict | None = None) -> dict[str, Any]:
        """Make a POST request to the IMA API.

        Args:
            endpoint: API endpoint path (e.g., 'knowledge/get_knowledge_list')
            payload: JSON body to send (field names should be snake_case)

        Returns:
            Response data dict. On error returns {"code": -1, "msg": "..."}.
        """
        url = f"{BASE_URL}{endpoint}"
        if payload is None:
            payload = {}

        # Only include client_id/api_key if we don't have a session token
        # (token-based auth uses headers, not body fields)
        if not self.token:
            if self.client_id and "client_id" not in payload:
                payload["client_id"] = self.client_id
            if self.api_key and "api_key" not in payload:
                payload["api_key"] = self.api_key

        try:
            resp = self._client.post(url, json=payload, headers=self._get_headers())
            data = resp.json()

            # Check if token expired (code 41 = login failed)
            code = data.get("code", 0)
            if code in (41, 100001, 100002, -1001, -1002):
                # Try to refresh token
                if self._try_refresh_token():
                    # Retry with new token
                    resp = self._client.post(
                        url, json=payload, headers=self._get_headers()
                    )
                    data = resp.json()
            return data
        except httpx.HTTPError as e:
            return {"code": -1, "msg": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"code": -1, "msg": f"Request error: {str(e)}"}

    def close(self):
        """Close the HTTP client."""
        self._client.close()
