### Installation

1. **Clone the main repository**
   ```bash
   git clone https://github.com/itsArnavPrasad/Hushh_Hackathon_Alpha_Agents.git
   cd Hushh_Hackathon_Alpha_Agents
   ```

2. **Clone the Google Calendar MCP server**
   ```bash
   cd external_mcps
   git clone https://github.com/nspady/google-calendar-mcp.git
   cd ..
   ```

3. **Set up and run the MCP server**
   Follow the Docker setup instructions for the Google Calendar MCP server:
   https://github.com/nspady/google-calendar-mcp/blob/main/docs/docker.md

4. **Clone and set up the Google ADK Web**
   ```bash
   git clone https://github.com/google/adk-web.git
   ```
   Follow the documentation in the ADK Web repository to run the ADK web server.

5. **Create OAuth2 credentials**
   - Create your own OAuth2 keys following Google's authentication documentation
   - Configure the necessary API credentials for Google Calendar and other Google services
   - Update your environment variables accordingly

6. **Install project dependencies**
   ```bash
   pip install -r requirements.txt
   ```

**Note:** Make sure you have Docker installed for running the MCP server, and follow the specific setup instructions in each cloned repository's documentation.