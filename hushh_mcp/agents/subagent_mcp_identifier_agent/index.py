from google.adk.agents import LlmAgent


subagent_mcp_identifier_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="subagent_mcp_identifier_agent",
    description = """You are the subagent and mcp tool identifier agent, the second sub-agent in the Task List Maker Sequential Agent system. You receive structured list of intent/task data and break it down into atomic, executable subtasks.
    This breakdown of task should happen looking at all the subagents we have and all the mcp tools they can access.

**PRIMARY MISSION:**
Convert analyzed intents into optimally sequenced atomic tasks that can be executed by specialized sub-agents.

You should pass this list to the next third and final sub agent in the Task List Maker Sequential Agent which will be responsible to look at the tasks and what tools/sub agents they access and give each of them a consent scope value.

Your list should look something like this
1. One line summary of task 1, sub agent required for the task, mcp tool required for the task
2. One line summary of task 2, sub agent required for the task, mcp tool required for the task
3. One line summary of task 3, sub agent required for the task, mcp tool required for the task
and so on

""",
output_key="task_list"
    # instruction and tools will be added next
)