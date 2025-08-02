# Consent-Driven Calendar Agentic System

## 🏆 Hackathon Project Overview

This project was developed for a hackathon focused on implementing **Hush's consent protocol** into agentic systems. Our team created a sophisticated calendar management system that prioritizes user consent at every step, ensuring that AI agents only perform actions with explicit user permission.

## 🎯 Project Vision

The core philosophy of our system is **"Consent First"** - no action is performed without explicit user authorization. We've built an agentic system that breaks down complex calendar tasks into atomic operations, each requiring individual consent through a robust trustlink mechanism.

## 🏗️ System Architecture

### Core Components

Our system is built around a **User Agent** that orchestrates multiple specialized sub-agents, all powered by Google's Agent Development Kit (ADK).

```
User Input → User Agent → Task Pipeline → Execution Loop → Calendar Operations
     ↓              ↓            ↓              ↓               ↓
 Raw Request → Task Analysis → Consent Flow → Trustlink → MCP Tools
```

### Agent Hierarchy

#### 1. **User Agent** (Root Orchestrator)
- **File**: `agents/user_agent.py`
- **Purpose**: Central coordinator that manages the entire workflow
- **Key Features**:
  - Fetches current date/time context using `fetch_date_time` operon
  - Routes requests to appropriate agent pipelines
  - Manages overall system state and user interaction

#### 2. **Task List Pipeline** (Sequential Agent)
A three-stage sequential pipeline that processes raw user requests:

##### 2.1 Intent Extractor Agent
- **File**: `agents/intent_extractor_agent.py`
- **Purpose**: Breaks down natural language requests into atomic tasks
- **Output**: Structured list of individual tasks (one CRUD operation per task)

##### 2.2 Sub-Agent MCP Tool Identifier Agent
- **File**: `agents/subagent_mcp_identifier_agent.py`
- **Purpose**: Maps each task to appropriate sub-agents and MCP tools
- **Features**:
  - Queries available MCP tools using `calendar_mcp_tool`
  - Assigns specific tools to each task
  - Prevents hallucination by only using verified tool data

##### 2.3 Scope Identifier Agent
- **File**: `agents/scope_identifier_agent.py`
- **Purpose**: Determines required consent scopes for each task
- **Integration**: Works with Hush consent framework to define permission levels

#### 3. **Calendar Executor Loop Agent**
- **File**: `agents/calendar_executor_loop_agent.py`
- **Purpose**: Orchestrates task execution with consent validation
- **Workflow**:
  1. Processes tasks sequentially (one at a time)
  2. Updates task status: `pending` → `in_progress` → `completed/failed`
  3. Coordinates between Trustlink Agent and Calendar Agent
  4. Manages state consistency across the workflow

#### 4. **Trustlink Agent**
- **File**: `agents/trustlink_agent.py`
- **Purpose**: Handles user consent and trustlink generation
- **Features**:
  - **Always asks for explicit user consent** before proceeding
  - Generates trustlinks using `generate_trustlink` operon
  - Blocks execution until consent is obtained
  - Creates delegation tokens for secure agent communication

#### 5. **Calendar Agent**
- **File**: `agents/calendar_agent.py`
- **Purpose**: Executes calendar operations via MCP tools
- **Security Features**:
  - **Always validates trustlinks** before any operation
  - Uses `validate_trustlink` operon for verification
  - Only processes tasks marked as "in_progress"
  - Connects to dockerized Google Calendar MCP server

## 🛡️ Consent & Security Framework

### Trustlink System
Our custom trustlink mechanism ensures secure delegation between agents:

- **Generation**: Created by Trustlink Agent after user consent
- **Validation**: Verified by Calendar Agent before execution
- **Scope**: Contains specific permissions for individual tasks
- **Security**: One-time use tokens that prevent unauthorized access

### Consent Scopes
Defined in `agents/calendar_agent/utils.py`:

```python
AGENT_GCAL_READ    # Read calendar data
AGENT_GCAL_WRITE   # Modify calendar data
```

### MCP Tool Registry
Our system supports the following Google Calendar operations:

| Tool | Description | Consent Scope |
|------|-------------|---------------|
| `list-calendars` | Fetch all accessible calendars | READ |
| `list-events` | Retrieve calendar events | READ |
| `search-events` | Search events by keywords/date | READ |
| `create-event` | Create new calendar events | WRITE |
| `update-event` | Modify existing events | WRITE |
| `delete-event` | Remove calendar events | WRITE |
| `list-colors` | Get available color codes | READ |

## 🔧 Technical Implementation

### Technology Stack

- **Framework**: Google Agent Development Kit (ADK)
- **Language**: Python
- **Consent Protocol**: Hush Framework
- **Calendar Integration**: Google Calendar MCP Server (Dockerized)
- **Architecture**: Multi-agent system with sequential pipelines

### Key Features

1. **Sequential Task Processing**: Tasks are executed one by one to maintain control and consent verification
2. **State Management**: Comprehensive task status tracking (pending/in_progress/completed/failed)
3. **Error Handling**: Retry mechanisms with graceful failure handling
4. **Consent Validation**: Multi-layer consent verification at every step
5. **Tool Isolation**: Each MCP tool requires specific consent scopes

### Custom Operons

We developed several custom operons (functions), although in our project we only use some of these for system operations:

- `generate_trustlink`: Creates secure delegation tokens
- `validate_trustlink`: Verifies token authenticity and scope
- `fetch_date_time`: Provides current temporal context
- `calendar_mcp_tool`: Tool registry and metadata management

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Docker (for Google Calendar MCP server)
- Google ADK installed
- Hush consent framework
- Google Calendar API credentials

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install google-adk hushh-mcp
   ```
3. Set up Google Calendar MCP server:
   ```bash
   docker run -p 3000:3000 [calendar-mcp-server]
   ```
4. Configure authentication credentials
5. Run the system:
   ```bash
   python agents/user_agent.py
   ```

## 📋 Usage Examples

### Basic Calendar Operations

```
User: "Schedule a meeting with John tomorrow at 2 PM"

System Flow:
1. Intent Extractor: Break into atomic tasks
2. Tool Identifier: Map to create-event tool
3. Scope Identifier: Assign WRITE permission
4. Trustlink Agent: Ask user consent
5. Calendar Agent: Execute after validation
```

### Complex Multi-step Operations

```
User: "Find my free time this week and schedule a team meeting"

System Flow:
1. Task 1: Search existing events (READ scope)
2. Task 2: Identify free slots (READ scope)  
3. Task 3: Create new meeting (WRITE scope)
Each task requires individual consent approval
```

## 🎯 Key Achievements

1. **Consent-First Architecture**: Every operation requires explicit user approval
2. **Atomic Task Decomposition**: Complex requests broken into manageable units
3. **Secure Agent Communication**: Trustlink system prevents unauthorized actions
4. **Flexible Tool Integration**: Modular MCP tool registry system
5. **Robust Error Handling**: Graceful failure recovery and user feedback

## 🔮 Future Enhancements

While we focused on core Google Calendar MCP tools for this hackathon, our operon registry includes additional functionality for future expansion:

- Advanced scheduling algorithms
- Multi-calendar synchronization
- Smart meeting suggestions
- Conflict resolution automation
- Integration with additional calendar providers

## 🏅 Hackathon Impact

This project demonstrates how consent protocols can be seamlessly integrated into agentic systems without sacrificing functionality. By prioritizing user control and transparent operations, we've created a model for ethical AI agent design that respects user privacy while delivering powerful automation capabilities.

## 🤝 Team & Technologies

- **Framework**: Google Agent Development Kit
- **Consent Protocol**: Hush Framework
- **Architecture**: Multi-agent sequential pipeline system
- **Deployment**: Dockerized MCP server infrastructure

---

**Built with ❤️ for the Hush Consent Protocol Hackathon**

*Demonstrating that powerful AI automation and user consent can work together seamlessly.*