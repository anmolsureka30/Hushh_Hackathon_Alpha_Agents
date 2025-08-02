from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from hushh_mcp.operons.generate_trustlink import generate_trustlink  

scope_indentifier_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="trustlink_agent",
    description = """
You are the Trustlink Agent, responsible for generating trustlinks after user consent. You will receive a task list from the previous agent and generate a trustlink for each task
""",
    tools=[
        FunctionTool(
            func=generate_trustlink,  # Assuming generate_trustlink is defined elsewhere
        )
    ],
)
