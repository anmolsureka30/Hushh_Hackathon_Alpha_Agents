from google.adk.tools import ToolContext
from google.genai import types
from typing import Optional, Dict, Any
import json
from hushh_mcp.trust.link import verify_trust_link, is_trusted_for_scope
from hushh_mcp.constants import ConsentScope
from hushh_mcp.types import TrustLink

async def validate_trustlink(
    trust_link: dict,
    required_scope: str,
) -> Dict[str, Any]:
    """
    Validates a TrustLink for a given scope.

    Args:
        trust_link (dict): The TrustLink object (as dict or pydantic).
        required_scope (str): The required scope for delegation.

    Returns:
        dict: {
            "is_valid": bool,
            "reason": str or None,
            "trust_link": dict or None
        }
    """
    # Validate scope
    try:
        if required_scope in ConsentScope.list():
            scope_enum = ConsentScope(required_scope)
        else:
            scope_enum = ConsentScope(required_scope)
    except Exception:
        scope_enum = required_scope

    # Convert to TrustLink object if needed
    if isinstance(trust_link, dict):
        trust_link_obj = TrustLink(**trust_link)
    else:
        trust_link_obj = trust_link

    is_valid = is_trusted_for_scope(trust_link_obj, scope_enum)
    reason = None
    if not is_valid:
        if not verify_trust_link(trust_link_obj):
            reason = "Invalid or expired trust link"
        elif trust_link_obj.scope != scope_enum:
            reason = f"Scope mismatch: link scope={trust_link_obj.scope}, required={scope_enum}"

    result = {
        "is_valid": is_valid,
        "reason": reason,
        "trust_link": trust_link_obj.dict() if hasattr(trust_link_obj, 'dict') else dict(trust_link_obj)
    }

    return result