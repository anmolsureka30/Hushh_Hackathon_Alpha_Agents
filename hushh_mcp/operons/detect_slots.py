
from google.adk.tools import ToolContext
from google.genai import types
from typing import List, Dict
from hushh_mcp.operons.mcp_adapter import get_freebusy
from hushh_mcp.operons.memory import CalendarAgentMemory
from hushh_mcp.operons.gemini_llm import gemini_chat
from hushh_mcp.operons.prompts import SUMMARIZE_CALENDAR_PROMPT
import json

from typing import Optional

async def detect_available_slots(
    user_id: str,
    calendar_ids: Optional[List[str]] = None,
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    explain: bool = False,
    tool_context: Optional[ToolContext] = None,
) -> dict:
    
    """
    Detect available free/busy slots for a user from their calendar(s).

    Args:
        user_id (str): The unique identifier for the user.
        calendar_ids (list, optional): List of calendar IDs to check. Defaults to all.
        time_min (str, optional): Start time (ISO format) for the search window.
        time_max (str, optional): End time (ISO format) for the search window.
        explain (bool, optional): Whether to provide a natural language explanation.
        tool_context (ToolContext, optional): The function context (provided by ADK).

    Returns:
        dict: {
            "status": "success",
            "free_busy": free/busy data,
            "explanation": (optional) LLM-generated summary,
            "artifact_error": error message if artifact saving fails (optional)
        }
    """
    free_busy = get_freebusy(
        user_id=user_id,
        calendar_ids=calendar_ids or [],
        time_min=time_min,
        time_max=time_max
    )
    memory = CalendarAgentMemory(user_id)
    memory.save_context("last_free_busy", free_busy)

    result = {
        "status": "success",
        "free_busy": free_busy
    }

    if explain:
        prompt = SUMMARIZE_CALENDAR_PROMPT.format(events=free_busy)
        explanation = gemini_chat(prompt)
        result["explanation"] = explanation

    # Optionally, save the free/busy data as an artifact (e.g., as JSON)
    if tool_context:
        try:
            await tool_context.save_artifact(
                "freebusy.json",
                types.Part.from_data(
                    data=json.dumps(free_busy, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            result["artifact_error"] = str(e)

    return result