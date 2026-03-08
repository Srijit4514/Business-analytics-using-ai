from typing import Any, Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2, description="Natural language question")


class LLMOutput(BaseModel):
    sql_query: str
    chart_type: str
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    description: Optional[str] = None
    error: Optional[str] = None


class QueryResponse(BaseModel):
    sql_query: str
    chart_type: str
    data: list[dict[str, Any]]
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    description: Optional[str] = None
    error: Optional[str] = None
