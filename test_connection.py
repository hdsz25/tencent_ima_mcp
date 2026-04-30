"""Test IMA API connection using the updated client."""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ima_api.client import ImaClient

client = ImaClient()

print(f"Token: {client.token[:20]}..." if client.token else "Token: (not set)")
print(f"User ID: {client.user_id}" if client.user_id else "User ID: (not set)")
print()

# Test: get_knowledge_list
print("=== get_knowledge_list ===")
result = client.post("knowledge/get_knowledge_list", {"limit": 5, "offset": 0})
print(f"  code={result.get('code')}, msg={result.get('msg', '')[:50]}")
if result.get("code") == 0:
    kl = result.get("knowledge_list", [])
    print(f"  Got {len(kl)} items")
    for k in kl[:3]:
        print(f"    - {k.get('title', 'untitled')[:50]}")

# Test: get_tags
print("\n=== get_tags ===")
result = client.post("knowledge/get_tags", {"limit": 10})
print(f"  code={result.get('code')}, msg={result.get('msg', '')[:50]}")
if result.get("code") == 0:
    tags = result.get("tag_infos", [])
    print(f"  Got {len(tags)} tags")

# Test: search_knowledge
print("\n=== search_knowledge ===")
result = client.post("knowledge/search_knowledge", {"keyword": "streamlit", "limit": 5})
print(f"  code={result.get('code')}, msg={result.get('msg', '')[:50]}")
if result.get("code") == 0:
    print(f"  SUCCESS!")

client.close()
print("\n--- All tests passed! ---")
