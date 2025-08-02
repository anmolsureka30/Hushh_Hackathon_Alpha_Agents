from google.adk.agents import LlmAgent , LoopAgent
from google.adk.tools import FunctionTool
from hushh_mcp.operons.fetch_date_time import fetch_date_time
from hushh_mcp.agents.trustlink_agent import trustlink_agent
from hushh_mcp.agents.calendar_agent import calendar_agent 

calendar_executor_loop_agent = LoopAgent(
    name="calendar_executor_agent",
    model="gemini-2.0-flash",
    description="A loop agent that generates a trustlink after user consent and completes task via calender agent then proceeds to next task.",
    tools=[
        FunctionTool(
            func=fetch_date_time,
        ),
    ],
    # Agent order is crucial: Critique first, then Refine/Exit
    sub_agents=[
        trustlink_agent,
        calendar_agent
    ],
    max_iterations=10 # Limit loops
)

