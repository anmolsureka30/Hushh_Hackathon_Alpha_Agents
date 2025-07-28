

from google.adk.tools import ToolContext
from google.genai import types

from hushh_mcp.operons.prompts import SUGGEST_SCHEDULE_PROMPT
from hushh_mcp.operons.gemini_llm import gemini_chat
import json

async def suggest_optimal_schedule(
    user_id: str,
    free_busy: dict,
    user_preferences: dict,
    tool_context: ToolContext,
) -> dict:
    """Suggest an optimal schedule for a user based on their free/busy slots and preferences.

    Args:
        user_id (str): The unique identifier for the user requesting the schedule.
        free_busy (dict): The user's free/busy information, typically from a calendar API.
        user_preferences (dict): The user's preferences for the task, such as time of day, duration, or other constraints.
        tool_context (ToolContext): The function context (provided by ADK).

    Returns:
        dict: A dictionary containing:
            - 'status': 'success' if a suggestion was generated, otherwise 'error'.
            - 'suggestion': The suggested schedule (if successful).
            - 'reason': Explanation or error message (if applicable).
    """
    prompt = SUGGEST_SCHEDULE_PROMPT.format(
        task_description=user_preferences.get("task", "No task provided"),
        free_slots=free_busy,
        preferences=user_preferences
    )
    suggestion_text = gemini_chat(prompt)
    try:
        suggestion = json.loads(suggestion_text)
        result = {
            "status": "success",
            "suggestion": suggestion
        }
        # Optionally, save the suggestion as an artifact (e.g., as JSON)
        try:
            await tool_context.save_artifact(
                "suggested_schedule.json",
                types.Part.from_data(
                    data=json.dumps(suggestion, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            # Log artifact saving error, but don't fail the tool
            result["artifact_error"] = str(e)
        return result
    except Exception:
        return {
            "status": "error",
            "reason": f"Could not parse suggestion: {suggestion_text}"
        }