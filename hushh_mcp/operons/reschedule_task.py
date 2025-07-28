
from google.adk.tools import ToolContext
from google.genai import types

from hushh_mcp.operons.prompts import RESCHEDULE_TASK_PROMPT
from hushh_mcp.operons.gemini_llm import gemini_chat
from hushh_mcp.operons.mcp_adapter import update_event
import json

async def reschedule_task(
    user_id: str,
    calendar_id: str,
    event_id: str,
    new_time: str,
    reason: str = None,
    event_details: str = None,
    user_intent: str = None,
    conflicts: str = None,
    tool_context: ToolContext = None,
) -> dict:
    """
    Suggests a new time for a calendar event using LLM reasoning, then updates the event.

    Args:
        user_id (str): The unique identifier for the user.
        calendar_id (str): The calendar's unique identifier.
        event_id (str): The event's unique identifier.
        new_time (str): The new time proposed for the event (ISO format).
        reason (str, optional): Reason for rescheduling.
        event_details (str, optional): Details about the event.
        user_intent (str, optional): User's intent for the reschedule.
        conflicts (str, optional): Any known conflicts.
        tool_context (ToolContext, optional): The function context (provided by ADK).

    Returns:
        dict: {
            "status": "rescheduled" or "error",
            "suggestion": dict with new_time and reason,
            "result": update result from MCP (if successful),
            "artifact_error": error message if artifact saving fails (optional)
        }
    """
    prompt = RESCHEDULE_TASK_PROMPT.format(
        event_details=event_details or "N/A",
        user_intent=user_intent or "N/A",
        conflicts=conflicts or "None"
    )
    suggestion_text = gemini_chat(prompt)
    try:
        suggestion = json.loads(suggestion_text)
    except Exception:
        suggestion = {"new_time": None, "reason": suggestion_text}

    update_result = None
    if suggestion.get("new_time"):
        update_result = update_event(
            user_id=user_id,
            calendar_id=calendar_id,
            event_id=event_id,
            new_time=suggestion["new_time"],
            reason=reason
        )

    result = {
        "status": "rescheduled" if suggestion.get("new_time") else "error",
        "suggestion": suggestion,
        "result": update_result,
    }

    # Optionally, save the suggestion as an artifact (e.g., as JSON)
    if tool_context:
        try:
            await tool_context.save_artifact(
                "reschedule_suggestion.json",
                types.Part.from_data(
                    data=json.dumps(suggestion, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            result["artifact_error"] = str(e)

    return result