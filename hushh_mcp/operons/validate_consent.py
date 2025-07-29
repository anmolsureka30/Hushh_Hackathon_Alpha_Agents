from google.adk.tools import ToolContext
from google.genai import types
from typing import Optional, Dict, Any
import json
from hushh_mcp.consent.token import validate_token
from hushh_mcp.constants import ConsentScope

async def validate_consent(
    token_str: str,
    required_scope: str,
    user_id: Optional[str] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """
    Validates a consent token for a given scope and (optionally) user.

    Args:
        token_str (str): The consent token string to validate.
        required_scope (str): The required scope for the action (should match ConsentScope values).
        user_id (str, optional): The user ID to check against the token (recommended for extra security).
        tool_context (ToolContext, optional): The function context (for artifact saving).

    Returns:
        dict: {
            "is_valid": bool,
            "reason": str or None,
            "token": dict or None
        }
    """
    # Use ConsentScope enum if possible
    try:
        if required_scope in ConsentScope.list():
            scope_enum = ConsentScope(required_scope)
        else:
            scope_enum = ConsentScope(required_scope)
    except Exception:
        scope_enum = required_scope

    is_valid, reason, parsed_token = validate_token(token_str, expected_scope=scope_enum)

    # Optionally check user_id
    if is_valid and user_id:
        if hasattr(parsed_token, 'user_id') and str(parsed_token.user_id) != str(user_id):
            is_valid = False
            reason = f"User ID mismatch: token user_id={parsed_token.user_id}, expected={user_id}"

    # Prepare result
    result = {
        "is_valid": is_valid,
        "reason": reason,
        "token": parsed_token.dict() if (parsed_token and hasattr(parsed_token, 'dict')) else None
    }

    # Save the result as an artifact if tool_context is provided
    if tool_context:
        try:
            await tool_context.save_artifact(
                "validate_consent_result.json",
                types.Part.from_data(
                    data=json.dumps(result, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            print(f"Error saving artifact: {e}")

    return result
