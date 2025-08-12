from typing import Optional
from pydantic import BaseModel, Field

class Page(BaseModel):
    data: Optional[list] = None
    total: Optional[int] = Field(default=None, description="Total number of items")
    page_number: Optional[int] = Field(default=None, description="Current page number")
    page_size: Optional[int] = Field(default=None, description="Number of items per page")
    error: Optional[str] = None
