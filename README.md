# Sonar-MCP
Sonar-MCP is a FastMCP-based service for searching SonarQube issues and retrieving rule definitions via HTTP.

# Prerequisites
* Python 3.11+
* Access to SonarQube instance and API token

# Setup
Clone the repository.

Install dependencies (if using pyproject.toml):

    pip install -r requirements.txt

Or, if using Poetry:

    poetry install

Create a .env file in the project root with your SonarQube credentials:


    SONAR_TOKEN=your-sonarqube-token
    SONAR_URL=https://your-sonarqube-url

# Running the Server
Start the MCP server:

    python3 server.py

The service will run with HTTP streaming enabled.

# Tools
* search_issues_tool: Search for issues in a specific file.
* get_rule_tool: Get the definition of a specific rule.
