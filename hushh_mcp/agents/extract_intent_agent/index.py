
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

extract_intent_agent = LlmAgent(
    name="ExtractIntentAgent",
    model="gemini-2.0-flash",
    instruction="""You are a expert assistant that extracts structured intent and required tasks workflow from user prompts for digital agents.

Return a JSON object with two keys: "intent" (the action) and "entities" (a dictionary of extracted entities).

Examples:
User: "Can you find free time tomorrow afternoon to meet with Ankit?"
Output: {"intent": "detect_slots", "entities": {"date": "tomorrow afternoon", "person": "Ankit"}}
""",
    description="Writes initial Python code based on a specification.",
    output_key="generated_code" # Stores output in state['generated_code']
)
