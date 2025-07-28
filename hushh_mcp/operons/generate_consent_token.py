from google.adk.tools import ToolContext
from google.genai import types
from typing import Optional, Dict, Any
import json
from hushh_mcp.consent.token import issue_token
from hushh_mcp.constants import ConsentScope
from hushh_mcp.types import HushhConsentToken

async def generate_consent_token(
    user_id: str,
    agent_id: str,
    scope: str,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Issues a scoped consent token for a user and agent using the ConsentScope enum.

    Args:
        user_id (str): The user who is granting consent.
        agent_id (str): The agent being authorized.
        scope (str): The scope of access (should match ConsentScope values).
        tool_context (ToolContext, optional): The function context (for artifact saving).

    Returns:
        dict: The issued consent token object (as dict).
    """
    # Validate scope is a valid ConsentScope or custom
    try:
        # Try to use ConsentScope enum for known scopes
        if scope in ConsentScope.list():
            scope_enum = ConsentScope(scope)
        else:
            # Allow custom scopes
            scope_enum = ConsentScope(scope)
    except Exception:
        # Fallback: treat as string
        scope_enum = scope

    # Issue the token
    token_obj: HushhConsentToken = issue_token(
        user_id=user_id,
        agent_id=agent_id,
        scope=scope_enum
    )

    # Convert to dict for output
    token_dict = token_obj.dict() if hasattr(token_obj, 'dict') else dict(token_obj)

    # Save the token as an artifact if tool_context is provided
    if tool_context:
        try:
            await tool_context.save_artifact(
                "consent_token.json",
                types.Part.from_data(
                    data=json.dumps(token_dict, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            print(f"Error saving artifact: {e}")

    return token_dict
