from google.adk.tools import ToolContext
from google.genai import types
from typing import Optional, Dict, Any
import json
from hushh_mcp.trust.link import revoke_trust_link
from hushh_mcp.types import TrustLink

async def revoke_trust(
    trust_link: dict,
) -> Dict[str, Any]:
    """
    Revokes a TrustLink (agent-to-agent delegation).

    Args:
        trust_link (dict): The TrustLink object (as dict or pydantic).

    Returns:
        dict: {
            "revoked": bool,
            "trust_link": dict,
            "error": str (if any)
        }
    """
    try:
        if isinstance(trust_link, dict):
            trust_link_obj = TrustLink(**trust_link)
        else:
            trust_link_obj = trust_link
        revoke_trust_link(trust_link_obj)
        result = {
            "revoked": True,
            "trust_link": trust_link_obj.dict() if hasattr(trust_link_obj, 'dict') else dict(trust_link_obj)
        }
    except Exception as e:
        result = {
            "revoked": False,
            "trust_link": trust_link,
            "error": str(e)
        }


    return result
