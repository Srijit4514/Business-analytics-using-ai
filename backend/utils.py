import json
import re
from typing import Any

from models import LLMOutput

ALLOWED_CHARTS = {"bar_chart", "line_chart", "pie_chart", "table"}


def parse_llm_json(raw_text: str) -> LLMOutput:
    text = raw_text.strip()
    fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced_match:
        text = fenced_match.group(1)

    if not text.startswith("{"):
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            text = json_match.group(0)

    try:
        payload: dict[str, Any] = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM returned non-JSON response: {exc}") from exc

    llm_output = LLMOutput(**payload)
    if llm_output.chart_type not in ALLOWED_CHARTS:
        llm_output.chart_type = "table"
    return llm_output


def validate_sql_query(sql_query: str) -> tuple[bool, str | None]:
    if not sql_query or not sql_query.strip():
        return False, "Empty SQL query"

    normalized = sql_query.strip().rstrip(";").strip().lower()
    if not normalized.startswith("select"):
        return False, "Only SELECT queries are allowed"

    forbidden = ["insert", "update", "delete", "drop", "alter", "create", "attach", "pragma", "replace"]
    if any(re.search(rf"\b{token}\b", normalized) for token in forbidden):
        return False, "Disallowed SQL keyword detected"

    if ";" in sql_query.strip().rstrip(";"):
        return False, "Multiple SQL statements are not allowed"

    return True, None
