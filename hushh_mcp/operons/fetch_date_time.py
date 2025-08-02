from google.adk.tools import ToolContext
from google.genai import types
from typing import Optional, Dict, Any
import json
from datetime import datetime
import pytz

async def fetch_date_time(
    timezone: Optional[str] = None,
    tool_context: Optional[ToolContext] = None,
) -> Dict[str, Any]:
    """
    Fetches the current date, time, and time zone.

    Args:
        timezone (str, optional): The timezone to use (e.g., 'Asia/Kolkata'). Defaults to system local time.
        tool_context (ToolContext, optional): The function context (for artifact saving).

    Returns:
        dict: {
            "date": "YYYY-MM-DD",
            "time": "HH:MM:SS",
            "timezone": "<tz>"
        }
    """
    try:
        if timezone:
            tz = pytz.timezone(timezone)
        else:
            tz = datetime.now().astimezone().tzinfo
        now = datetime.now(tz)
        result = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "timezone": str(now.tzinfo)
        }
    except Exception as e:
        result = {
            "error": str(e)
        }

    if tool_context:
        try:
            await tool_context.save_artifact(
                "current_datetime.json",
                types.Part.from_data(
                    data=json.dumps(result, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            result["artifact_error"] = str(e)

    return result
