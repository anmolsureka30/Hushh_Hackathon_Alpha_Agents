from hushh_mcp.constants import ConsentScope
from google.adk.tools import ToolContext
from typing import Optional, List, Dict, Any

# ==================== Tool Metadata Schema ====================

class ToolMetadata:
    def __init__(self, name, description, consent_scope):
        self.name = name
        self.description = description
        self.consent_scope = consent_scope

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            # "required_consent_scopes": [scope.value for scope in self.consent_scope]
            "required_consent_scope": self.consent_scope
        }

# ==================== MCP Tool Registry ====================

TOOL_REGISTRY = {
    "list-calendars": ToolMetadata(
        name="list-calendars",
        description="Fetches a list of all calendars the user has access to.",
        consent_scope=[ConsentScope.AGENT_GCAL_READ]
    ),
    "list-events": ToolMetadata(
        name="list-events",
        description="Retrieves all events from a specified calendar.",
        consent_scope=[ConsentScope.AGENT_GCAL_READ]
    ),
    "search-events": ToolMetadata(
        name="search-events",
        description="Searches calendar events by keywords, date range, or participants.",
        consent_scope=[ConsentScope.AGENT_GCAL_READ]
    ),
    "create-event": ToolMetadata(
        name="create-event",
        description="Creates a new event in a user's calendar.",
        consent_scope=[ConsentScope.AGENT_GCAL_WRITE]
    ),
    "update-event": ToolMetadata(
        name="update-event",
        description="Updates an existing calendar event with new details.",
        consent_scope=[ConsentScope.AGENT_GCAL_WRITE]
    ),
    "delete-event": ToolMetadata(
        name="delete-event",
        description="Deletes a specified calendar event.",
        consent_scope=[ConsentScope.AGENT_GCAL_WRITE]
    ),
    # "get-freebusy": ToolMetadata(
    #     name="get-freebusy",
    #     description="Returns availability (free/busy) slots for specified calendars.",
    #     consent_scope=[ConsentScope.AGENT_GCAL_READ]
    # ),
    "list-colors": ToolMetadata(
        name="list-colors",
        description="Lists available calendar color codes for event categorization.",
        consent_scope=[ConsentScope.AGENT_GCAL_READ]
    ),
}

# ==================== Google ADK Single Tool ====================

async def calendar_mcp_tool(
    action: str,
    tool_name: Optional[str] = None,
    consent_scope: Optional[str] = None,
    tool_context: Optional[ToolContext] = None
) -> Any:
    """
    Google ADK tool for calendar tool metadata registry.

    Args:
        action (str): One of "get_tool_metadata", "list_all_tools", "get_tools_by_scope".
        tool_name (str, optional): Tool name for "get_tool_metadata".
        consent_scope (str, optional): Consent scope for "get_tools_by_scope".
        tool_context (ToolContext, optional): ADK context.

    Returns:
        dict or list: Tool metadata or list of tool metadata.
    """
    if action == "get_tool_metadata":
        if not tool_name:
            raise ValueError("tool_name is required for get_tool_metadata")
        tool = TOOL_REGISTRY.get(tool_name)
        if not tool:
            raise ValueError(f"No metadata found for tool: {tool_name}")
        return tool.as_dict()

    elif action == "list_all_tools":
        # Return only name and description for each tool
        return [
            {
                "agent": "calendar_agent",
                "tools": [
                    {"name": tool.name, "description": tool.description}
                    for tool in TOOL_REGISTRY.values()
                ]
            }
    
        ]

    elif action == "get_scope_for_tool":
        if not tool_name:
            raise ValueError("tool_name is required for get_scope_for_tool")
        tool = TOOL_REGISTRY.get(tool_name)
        if not tool:
            raise ValueError(f"No metadata found for tool: {tool_name}")
        # Return the list of consent scope values for the tool
        return [scope.value for scope in tool.consent_scope]

    else:
        raise ValueError(f"Unknown action: {action}")