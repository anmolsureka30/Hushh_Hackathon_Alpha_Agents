from google.adk.agents import LlmAgent


intent_extractor_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="intent_extractor_agent",
    description = """You are the Intent Analyzer, the first sub-agent in the Task List Maker Sequential Agent system. Your role is to parse and understand user requests with high accuracy and completeness.

**PRIMARY MISSION:**
Transform natural language user requests into structured intent data that enables precise task decomposition.
You have to break down the task into sub tasks. One task shouldnt be responsible for more than one CRUD operation.

The list should look something like this:
1. One line summary of task 1
2. One line summary of task 2
3. One line summary of task 3
and so on

""",
output_key="task_list"
    # instruction and tools will be added next
)