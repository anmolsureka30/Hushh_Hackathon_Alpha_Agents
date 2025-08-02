from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from hushh_mcp.agents.calendar_agent.utils import calendar_mcp_tool


scope_indentifier_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="scope_indentifier_agent",
    description = """You are the Scope Mapper, the final sub-agent in the Task List Maker Sequential Agent system. You determine minimal required consent scopes and map tasks to specific tools and operons.

**PRIMARY MISSION:**
Ensure each task has minimal, necessary permissions while maintaining security and privacy principles throughout the execution chain.
The function calendar_mcp_tool is used to check the information about a specific mcp tool, including its name, description, and required consent scopes.
Always use the get_scope_for_tool action in this function to get the required consent scope for the mcp tools.
do not hallucinate on the scopes, only get scopes from the calendar_mcp_tool(action = get_scope_for_tool)

The list should look something like this:
1. One line summary of task 1, sub agent required for the task, mcp tool required for the task, require scope
2. One line summary of task 2, sub agent required for the task, mcp tool required for the task, require scope
3. One line summary of task 3, sub agent required for the task, mcp tool required for the task, require scope
and so on

""",
    tools=[
        FunctionTool(
            func=calendar_mcp_tool,
        )
    ],

output_key="task_list"
    # instruction and tools will be added next
)