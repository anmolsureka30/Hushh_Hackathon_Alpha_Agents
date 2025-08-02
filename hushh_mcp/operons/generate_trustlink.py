from google.adk.tools import ToolContext
from google.genai import types
from typing import Optional, Dict, Any
import json
from hushh_mcp.trust.link import create_trust_link
from hushh_mcp.constants import ConsentScope
from hushh_mcp.types import TrustLink

async def generate_trustlink(
    from_agent: str,
    to_agent: str,
    scope: str,
    signed_by_user: str,
    expires_in_ms: Optional[int] = None,

) -> Dict[str, Any]:
    """
    Issues a TrustLink for agent-to-agent delegation.

    Args:
        from_agent (str): The delegating agent.
        to_agent (str): The delegatee agent.
        scope (str): The scope of delegation (should match ConsentScope values).
        signed_by_user (str): The user authorizing the delegation.
        expires_in_ms (int, optional): Custom expiry in ms.


    Returns:
        dict: The issued TrustLink object (as dict).
    """
    # Validate scope
    try:
        if scope in ConsentScope.list():
            scope_enum = ConsentScope(scope)
        else:
            scope_enum = ConsentScope(scope)
    except Exception:
        scope_enum = scope

    # Create the trust link
    if expires_in_ms is not None:
        trust_link: TrustLink = create_trust_link(
            from_agent=from_agent,
            to_agent=to_agent,
            scope=scope_enum,
            signed_by_user=signed_by_user,
            expires_in_ms=expires_in_ms
        )
    else:
        trust_link: TrustLink = create_trust_link(
            from_agent=from_agent,
            to_agent=to_agent,
            scope=scope_enum,
            signed_by_user=signed_by_user
        )

    trust_link_dict = trust_link.dict() if hasattr(trust_link, 'dict') else dict(trust_link)



    return trust_link_dict