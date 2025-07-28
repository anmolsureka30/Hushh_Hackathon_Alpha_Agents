from hushh_mcp.consent.token import validate_token
from hushh_mcp.constants import ConsentScope
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools import google_search
from hushh_mcp.agents.calendar_agent.index import calendar_agent

# Create parent agent and assign children via sub_agents
root_agent = LlmAgent(
    name="user_interaction_agent",
    model="gemini-2.0-flash",
    description="I am responsible for interacting with the user at the frontend and then delegating the tasks to my subagents",
    sub_agents=[ # Assign sub_agents here
        calendar_agent
    ]
)