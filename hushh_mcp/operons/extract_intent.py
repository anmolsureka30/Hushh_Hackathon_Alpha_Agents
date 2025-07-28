from google.adk.tools import ToolContext
from google.genai import types
from typing import Dict, Any
import json

# Example few-shot prompt for intent extraction
EXTRACT_INTENT_PROMPT = '''
You are an expert assistant that extracts structured intent and entities from user prompts for digital agents.

Return a JSON object with two keys: "intent" (the action) and "entities" (a dictionary of extracted entities).

Examples:
User: "Can you find free time tomorrow afternoon to meet with Ankit?"
Output: {"intent": "detect_slots", "entities": {"date": "tomorrow afternoon", "person": "Ankit"}}

User: "Reschedule my meeting with Ankit to 2pm next Wednesday."
Output: {"intent": "reschedule_event", "entities": {"event_name": "meeting with Ankit", "new_time": "2pm next Wednesday"}}

User: "Book a table for two at an Italian restaurant tonight."
Output: {"intent": "book_table", "entities": {"party_size": 2, "cuisine": "Italian", "datetime": "tonight"}}

User: "Add a call with Dr. Smith to my calendar on Friday at 10am."
Output: {"intent": "add_event", "entities": {"event": "call with Dr. Smith", "date": "Friday", "time": "10am"}}

Now extract the intent and entities from this user prompt:
User: "{prompt}"
Output:
'''

from hushh_mcp.operons.gemini_llm import gemini_chat

async def extract_intent(prompt: str, tool_context: ToolContext = None) -> Dict[str, Any]:
    """
    Extracts structured intent (action + entities) from a user prompt using an LLM.

    Args:
        prompt (str): The user prompt to analyze.
        tool_context (ToolContext, optional): The function context (for artifact saving).

    Returns:
        dict: {"intent": <action>, "entities": {<entity>: <value>, ...}}
    """
    # Compose the prompt for the LLM
    llm_prompt = EXTRACT_INTENT_PROMPT.format(prompt=prompt)
    llm_response = gemini_chat(llm_prompt)

    # Try to parse the LLM response as JSON
    try:
        result = json.loads(llm_response)
    except Exception:
        # Fallback: try to extract JSON substring
        import re
        match = re.search(r'\{.*\}', llm_response, re.DOTALL)
        if match:
            try:
                result = json.loads(match.group(0))
            except Exception:
                result = {"intent": None, "entities": {}}
        else:
            result = {"intent": None, "entities": {}}

    # Save the LLM output as an artifact if tool_context is provided
    if tool_context:
        try:
            await tool_context.save_artifact(
                "intent_extraction.json",
                types.Part.from_data(
                    data=json.dumps(result, indent=2),
                    mime_type="application/json"
                ),
            )
        except Exception as e:
            print(f"Error saving artifact: {e}")

    return result
