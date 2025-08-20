# Sonar-MCP
Sonar-MCP is a FastMCP-based service for searching SonarQube issues and retrieving rule definitions via HTTP.

# Prerequisites
* Python 3.11+
* Access to SonarQube instance and API token

# Setup
Clone the repository.

Create and activate a venv in the project

    python3 -m venv .venv
    source .venv/bin/activate

Install uv

    pip install uv

Install dependencies

    uv sync

Create a .env file in the project root with your SonarQube token and the SonarQube url:

    SONAR_TOKEN=your-sonarqube-token
    SONAR_URL=https://your-sonarqube-url

# Running the Server
Start the MCP server:

    python3 server.py

The service will start listening to 127.0.0.1 at port 8000. Exposes HTTP streaming server with no authentication.

# Tools
* search_issues_tool: Search for issues in a specific file.
* get_rule_tool: Get the definition of a specific rule.

# Example Prompt

    Search for and fix the sonar issues for the current file. Use the relative path of the file starting from and including the __PROJECT_ROOT__ directory, not the full path. Use 'SONAR_PROJECT_ID' as the project.
