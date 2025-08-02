# agents/user_agent.py

from hushh_mcp.consent.token import validate_token
from hushh_mcp.constants import ConsentScope
from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools import google_search
from hushh_mcp.agents.calendar_agent.index import calendar_agent
from hushh_mcp.agents.task_list_pipeline.index import task_list_pipeline
from google.adk.tools import FunctionTool
from hushh_mcp.operons.extract_intent import extract_intent
from hushh_mcp.operons.route_agent import route_agent
from hushh_mcp.operons.find_consent_scope import find_consent_scope
from hushh_mcp.operons.generate_trustlink import generate_trustlink
from hushh_mcp.operons.fetch_date_time import fetch_date_time
from hushh_mcp.agents.calendar_executor_loop_agent.index import calendar_executor_loop_agent

# Create parent agent and assign children via sub_agents
root_agent = LlmAgent(
    name="user_interaction_agent",
    model="gemini-2.0-flash",
    description="""You are a highly intelligent assistant that helps users manage their time, meetings, and calendar using AI agents. 
    Your goal is to understand the user's request, extract the task (intent), determine what kind of permission (consent) is needed, and delegate the task securely to the right calendar agent. 
    Keep in mind always fetch the date, time, and time zone using `fetch_date_time` tool before proceeding with any task.
    
    CRITICAL SEQUENTIAL WORKFLOW - YOU MUST FOLLOW THIS EXACT ORDER:
    
    1. INITIAL UNDERSTANDING:
       - Understand if the user is just talking or requesting action
       - If just talking, reply normally and stop
       - If requesting action, proceed to step 2
    
    2. TASK BREAKDOWN (ONE TIME ONLY):
       - Call the task_list_pipeline agent to break down the user request into smaller tasks
       - You MUST use task_list_pipeline - never create the list yourself
       - Store the returned task list for sequential processing
    
    3. SEQUENTIAL TASK PROCESSING (FOR EACH TASK ONE BY ONE):
      Send the task list to the calendar_executor_loop_agent, which will handle the sequential processing of each task.       
      
    4. COMPLETION:
       - After all tasks are processed, provide a summary of what was accomplished
    
    IMPORTANT RULES:
    - Always fetch the current date, time, and time zone using `fetch_date_time` operon before proceeding with any task
    - Process tasks SEQUENTIALLY, not in parallel
    - after the task_pipeline agent has broken down the tasks along with the subagents operons and scopes , send them to the calendar_executor_loop_agent
    - The calendar_executor_loop_agent will handle the orchestration of tasks, including trustlink generation and validation, and will ensure proper consent flow for each individual task.    
    Your goal is to help users automate their calendar and scheduling needs with maximum precision, minimum permissions, and zero friction while ensuring proper consent flow for each individual task.""",

    tools=[
        FunctionTool(
            func=fetch_date_time,
        )
    ],
    sub_agents=[ # Assign sub_agents here
        calendar_executor_loop_agent,  # This is the orchestrator agent
        task_list_pipeline
    ],
)