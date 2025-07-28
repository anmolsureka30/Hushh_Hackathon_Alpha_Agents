from hushh_mcp.consent.token import validate_token
from hushh_mcp.constants import ConsentScope
from hushh_mcp.operons.gcal_sync import get_freebusy
from hushh_mcp.operons.suggest_schedule import suggest_optimal_schedule
from hushh_mcp.operons.detect_slots import detect_available_slots

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

calendar_agent = LlmAgent(
    name="calendar_agent",
    model="gemini-2.0-flash", 
    instruction="You are a helpful assistant. Answer user questions using Google Search when needed.",
    description="An agent which facilitates interaction with a calendar like google calendar",
    # tools=[google_search] add mcp here
    tools=[
        FunctionTool(
            func=suggest_optimal_schedule,
        ),
        FunctionTool(
            func=detect_available_slots,
        ),
        MCPToolset(
            connection_params=StreamableHTTPServerParams(
                url='http://localhost:3000/',
            ),
            # don't want agent to do write operation
            # you can also do below
            # tool_filter=lambda tool, ctx=None: tool.name
            # not in [
            #     'write_file',
            #     'edit_file',
            #     'create_directory',
            #     'move_file',
            # ],
            tool_filter=[
                'list-calendars',
                'list-events',
                'search-events',
                'create-event',
                'update-event',
                'delete-event',
                'get-freebusy',
                'list-colors',
            ],
        )
    ],
)

_all_ = ['calendar_agent']