from hushh_mcp.consent.token import validate_token
from hushh_mcp.constants import ConsentScope
from hushh_mcp.operons.gcal_sync import get_freebusy
from hushh_mcp.operons.suggest_schedule import suggest_optimal_schedule
from hushh_mcp.operons.detect_slots import detect_available_slots
from hushh_mcp.operons.validate_trustlink import validate_trustlink

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

calendar_agent = LlmAgent(
    name="calendar_agent",
    model="gemini-2.0-flash", 
    description="An agent which facilitates interaction with google calendar.",
    instruction="""
    An agent which facilitates interaction with google calendar. 
    You will receive a task from the previous agent, you have to focus on the task whose status is "in_progress".
    ONLY DO THE TASK WHICH IS IN_PROGRESS.
    You will receive a trustlink from the previous agent, you have to validate the trustlink
    ALWAYS CALL THE VALIDATE_TRUSTLINK OPERON BEFORE ANY OPERATION TO ENSURE THE USER HAS GIVEN CONSENT.
    If the trustlink is not valid, do not proceed with any operation.
    If the trustlink is valid, proceed with the operation.
    IMPORTANT: You must always validate the trustlink before proceeding with any operation.
    PERFORM ONLY ONE TASK PER VALIDATION OF TRUSTLINK.
    AS Soon AS MCP Is CALLED AND TASK IS COMPLETED , Transfer TO CALENDAR_EXECUTOR_LOOP_AGENT 
  
    """,
    tools=[
        FunctionTool(
            func=validate_trustlink,
        ),
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url='http://localhost:3000/',
            ),
            tool_filter=[
                'list-calendars',
                'list-events',
                'search-events',
                'create-event',
                'update-event',
                'delete-event',
                # 'get-freebusy',
                'list-colors',
            ],
        )
    ],
)

_all_ = ['calendar_agent']