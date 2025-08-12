from pydantic import BaseModel, Field

class SonarIssue(BaseModel):
    rule_key: str = Field(description="The rule that was violated")
    severity: str = Field(description="The severity of the issue")
    start_line: int = Field(description="The starting line of the issue")
    end_line: int = Field(description="The ending line of the issue")
    start_offset: int = Field(description="The starting offset of the issue")
    end_offset: int = Field(description="The ending offset of the issue")
    message: str = Field(description="The message describing the issue")