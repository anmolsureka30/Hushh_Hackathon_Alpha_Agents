from google.adk.tools import ToolContext
from google.genai import types
from typing import Optional
import json
from hushh_mcp.constants import ConsentScope

# Intent to consent scope mapping table (modular, using ConsentScope enum)
INTENT_TO_SCOPE = {
    "reschedule_event": ConsentScope.AGENT_GCAL_WRITE.value,
    "detect_slots": ConsentScope.AGENT_GCAL_READ.value,
    "suggest_schedule": ConsentScope.AGENT_GCAL_READ.value,
    # Add more mappings as needed, always using ConsentScope enum
}

async def find_consent_scope(intent: str, tool_context: Optional[ToolContext] = None) -> Optional[str]:
    """
    Maps an intent string to the minimum required consent scope using ConsentScope enum.

    Args:
        intent (str): The intent/action to resolve scope for.
        tool_context (ToolContext, optional): The function context (for artifact saving).

    Returns:
        str or None: The minimum required consent scope for the intent, or None if not found.
    """
    scope = INTENT_TO_SCOPE.get(intent, None)

    # Save the mapping as an artifact if tool_context is provided
    if tool_context:
        try:
            await tool_context.save_artifact(
                "resolve_consent_scope.json",
                types.Part.from_data(
                    data=json.dumps({"intent": intent, "scope": scope}, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            print(f"Error saving artifact: {e}")

    return scope
