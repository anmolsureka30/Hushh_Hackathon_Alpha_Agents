from google.adk.agents import Agent, SequentialAgent
from hushh_mcp.agents.intent_extractor_agent.index import intent_extractor_agent
from hushh_mcp.agents.subagent_mcp_identifier_agent.index import subagent_mcp_identifier_agent
from hushh_mcp.agents.scope_identifier_agent.index import scope_indentifier_agent

task_list_pipeline = SequentialAgent(
    name="task_list_pipeline",
    sub_agents=[
        intent_extractor_agent,
        subagent_mcp_identifier_agent,
        scope_indentifier_agent
        ],
    description="Transform complex user intents into structured, sequential task lists that can be executed by specialized sub-agents with appropriate consent scopes.",
    # The agents will run in the order provided: intent_extractor_agent -> subagent_mcp_identifier_agent -> scoping_agent
)