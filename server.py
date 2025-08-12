from mcp.server.fastmcp import FastMCP
from sonar_service import get_rule, search_issues
from models.page import Page
from urllib.parse import unquote

mcp = FastMCP(name='Sonar-MCP', stateless_http=True, debug=True, log_level='DEBUG')

@mcp.tool(description='Search for issues in a specific file', annotations={
    "project": "The project key. Example: com.truste.gda:gda", 
    "file": "The relative file path. Example: gda-app/src/main/java/com/truste/gda/asset/controller/AssetController.java", 
    "rule_key": "The rule key. Optional. Example: java:S6813",
    "page_number": "The page number starting from 1. Default 1", 
    "page_size": "The page size. Default 10"
})
def search_issues_tool(project: str, file: str, rule_key: str, page_number: int, page_size: int) -> Page:
    return search_issues(project, file, rule_key, page_number, page_size)

@mcp.tool(description='Get the definition of a specific rule', annotations={
    "rule_key": "The rule key. Optional. Example: java:S6813"
})
def get_rule_tool(rule_key: str) -> str:
    rule_key = unquote(rule_key)
    return get_rule(rule_key)

def main():
    mcp.run(transport='streamable-http')

if __name__ == "__main__":
    main()


