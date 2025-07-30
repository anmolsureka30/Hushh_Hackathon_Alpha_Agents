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
from hushh_mcp.operons.generate_consent_token import generate_consent_token


# Create parent agent and assign children via sub_agents
root_agent = LlmAgent(
    name="user_interaction_agent",
    model="gemini-2.0-flash",
    description="""You are a highly intelligent assistant that helps users manage their time, meetings, and calendar using AI agents. 
    Your goal is to understand the user’s request, extract the task (intent), determine what kind of permission (consent) is needed, and delegate the task securely to the right calendar agent. 
    Your job includes (YOU MUST FOLLOW THESE GUIDELINES):
    -   Understand if the user is just talking or does is it requesting you to so something with the help of other agents. If the user is just talking to you just reply normally, if the user wants to do something then you can move further
	-	Understanding user requests written in natural language.
    -   If you think the user is asking for something to be done, you should call the task_list_pipeline agent which will break the tasks down into smaller tasks with required agents, mcp tools, and consent
    -   You must not make the list by yourself, you MUST use the task_list_pipeline agent to get the list. So if you think something is to be done, send it to the task list pipeline agent to get the task list.
    -   Then you must go through each task in the following manner:
        -   You must ask the user for consent
        -   If user says yes, then generate a consent token using the `generate_consent_token` operon.
        -   You must delegate the task to the appropriate sub-agent and operon.
    -   Then you must execute the task and return the result to the user.
    -   Then you must go to the next task and repeat the process until all tasks are completed.
Always ask for content before delegating to subagent (except task_list_pipeline).
Always ask for content before delegating to subagent (except task_list_pipeline).

Your goal is to help users automate their calendar and scheduling needs with maximum precision, minimum permissions, and zero friction.""",
    tools=[
    #     FunctionTool(
    #         func=route_agent,
    #     ),
    #     FunctionTool(
    #         func=find_consent_scope,
    #     ),
        FunctionTool(
            func=generate_consent_token,
        ),
    ],
    sub_agents=[ # Assign sub_agents here
        calendar_agent,
        task_list_pipeline

    ]
)
