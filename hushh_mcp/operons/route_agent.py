from google.adk.tools import ToolContext
from google.genai import types
from typing import Dict, Any
import json

# Intent to agent/operon mapping table
INTENT_TO_AGENT_OPERON = {
    "reschedule_event": {"agent_name": "calendar_agent", "operon": "reschedule_events"},
    "detect_slots": {"agent_name": "calendar_agent", "operon": "detect_available_slots"},
    "suggest_schedule": {"agent_name": "calendar_agent", "operon": "suggest_optimal_schedule"},
    "lookup_contact": {"agent_name": "crm_agent", "operon": "get_contact_info"},
    # Add more mappings as needed
}

async def route_agent(intent: str, tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Maps an intent string to the correct sub-agent and operon name.

    Args:
        intent (str): The intent/action to route.
        tool_context (ToolContext, optional): The function context (for artifact saving).

    Returns:
        dict: {"agent_name": <agent>, "operon": <operon>}
    """
    # Look up the mapping
    mapping = INTENT_TO_AGENT_OPERON.get(intent, {"agent_name": None, "operon": None})

    # Save the mapping as an artifact if tool_context is provided
    if tool_context:
        try:
            await tool_context.save_artifact(
                "route_agent.json",
                types.Part.from_data(
                    data=json.dumps({"intent": intent, **mapping}, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            print(f"Error saving artifact: {e}")

    return mapping
