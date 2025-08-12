import requests
from models.page import Page
from models.sonar_issue import SonarIssue
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('SONAR_TOKEN')
URL = os.getenv('SONAR_URL')


def search_issues(project, file, rule_key, page_number, page_size) -> Page:
    search_url = f"{URL}/api/issues/search"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    params = {
        'components': f"{project}:{file}",
        'p': page_number,
        'ps': page_size
    }
    if rule_key:
        params['rules'] = rule_key
    try:
        response = requests.get(search_url, headers=headers, params=params)
        print(response.json())
        if response.status_code == 200:
            return Page(data=convert_response(response.json()), total=response.json().get('total', 0), page_number=page_number, page_size=page_size)
        else:
            return Page(error="Failed to retrieve issues")
    except Exception as e:
        return Page(error=f"Exception occurred: {str(e)}")
    
def convert_response(response_json):
    issues = response_json['issues']
    # issues is an array of sonar issues with the following structure:
    """ {
    "key": "19f8314e-7d68-4e83-8f7d-d79ae60ad85f",
    "rule": "java:S6813",
    "severity": "MAJOR",
    "component": "com.truste.gda:gda:gda-app/src/main/java/com/truste/gda/asset/controller/AssetController.java",
    "project": "com.truste.gda:gda",
    "line": 87,
    "hash": "22abdf4b55679d6d8e58b48500963e17",
    "textRange": {
        "startLine": 87,
        "endLine": 87,
        "startOffset": 4,
        "endOffset": 14
    },
    "flows": [],
    "status": "OPEN",
    "message": "Remove this field injection and use constructor injection instead.",
    "effort": "5min",
    "debt": "5min",
    "author": "loaner@ip-192-168-1-9.us-west-2.compute.internal",
    "tags": [],
    "creationDate": "2022-07-10T07:26:33+0000",
    "updateDate": "2024-07-16T02:40:40+0000",
    "type": "CODE_SMELL",
    "scope": "MAIN",
    "quickFixAvailable": false,
    "messageFormattings": [],
    "codeVariants": [],
    "cleanCodeAttribute": "CONVENTIONAL",
    "cleanCodeAttributeCategory": "CONSISTENT",
    "impacts": [
        {
        "softwareQuality": "MAINTAINABILITY",
        "severity": "MEDIUM"
        },
        {
        "softwareQuality": "RELIABILITY",
        "severity": "MEDIUM"
        }
    ],
    "issueStatus": "OPEN",
    "prioritizedRule": false
    } """
    # extract only the following fields: key, rule, severity, component, project, line, message
    extracted_issues = []
    for issue in issues:
        extracted_issues.append(SonarIssue(
            key=issue['key'],
            rule_key=issue['rule'],
            severity=issue['severity'],
            start_line=issue['textRange']['startLine'],
            end_line=issue['textRange']['endLine'],
            start_offset=issue['textRange']['startOffset'],
            end_offset=issue['textRange']['endOffset'],
            message=issue['message']
        ))
    return extracted_issues

def get_rule(rule_key: str) -> str:
    search_url = f"{URL}/api/rules/show"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    params = {
        'key': rule_key,
    }

    try:
        response = requests.get(search_url, headers=headers, params=params)
        if response.status_code == 200 and 'rule' in response.json():
            rule = response.json()['rule']
            response_text = f"{rule['key']}:{rule['name']}\n\n{convert_sections(rule['descriptionSections'])}"
            return response_text
        else:
            return "Failed to retrieve rule"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

def convert_sections(descriptionSections):
    """ {
            "key": "how_to_fix",
            "content": "<p>Use constructor injection instead.</p>\n<p>By using constructor injection, the dependencies are explicit and must be passed during an object’s construction. This avoids the possibility of\ninstantiating an object in an invalid state and makes types more testable. Fields can be declared final, which makes the code easier to understand, as\ndependencies don’t change after instantiation.</p>\n\n<h4>Noncompliant code example</h4>\n<pre data-diff-id=\"1\" data-diff-type=\"noncompliant\">\npublic class SomeService {\n    @Autowired\n    private SomeDependency someDependency; // Noncompliant\n\n    private String name = someDependency.getName(); // Will throw a NullPointerException\n}\n</pre>\n<h4>Compliant solution</h4>\n<pre data-diff-id=\"1\" data-diff-type=\"compliant\">\npublic class SomeService {\n    private final SomeDependency someDependency;\n    private final String name;\n\n    @Autowired\n    public SomeService(SomeDependency someDependency) {\n        this.someDependency = someDependency;\n        name = someDependency.getName();\n    }\n}\n</pre>"
    } """
    # merge all content into a single string
    merged_content = "\n\n".join(section["content"] for section in descriptionSections)
    return merged_content

def main():
    print('------')
    print(
        search_issues(
            'com.truste.gda:gda', 
            'gda-app/src/main/java/com/truste/gda/asset/controller/AssetController.java', 
            'java:S6813',
            1, 
            5)
    )
    print('------')
    print(
        get_rule('java:S6813')
    )
    print('------')

if __name__ == "__main__":
    main()