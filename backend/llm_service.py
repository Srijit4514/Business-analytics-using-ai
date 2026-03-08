import logging

import google.generativeai as genai

from config import API_KEY, GEMINI_MODEL
from models import LLMOutput
from utils import parse_llm_json

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are an expert SQL generation assistant for business intelligence.

Rules:
1) Use ONLY the provided database schema.
2) Generate ONLY valid SQLite SQL.
3) Return read-only SQL (SELECT only).
4) Never hallucinate tables or columns.
5) Recommend chart type from: bar_chart, line_chart, pie_chart, table.
6) Return output as JSON only.

Expected JSON format:
{
  "sql_query": "SELECT ...",
  "chart_type": "bar_chart | line_chart | pie_chart | table",
  "x_axis": "...",
  "y_axis": "...",
  "description": "...",
  "error": null
}
""".strip()


def generate_sql_with_gemini(question: str, schema_text: str) -> LLMOutput:
    logger.info("Generating SQL via Gemini")

    if not API_KEY:
        logger.warning("Gemini API key is not configured")
        return LLMOutput(
            sql_query="",
            chart_type="table",
            error="Gemini API key is missing. Set API_KEY in config.py",
        )

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)

    prompt = f"""
{SYSTEM_PROMPT}

Database schema:
{schema_text}

User question:
{question}
""".strip()

    response = model.generate_content(prompt)
    response_text = (response.text or "").strip()

    try:
        llm_output = parse_llm_json(response_text)
    except Exception as exc:
        logger.exception("Failed to parse Gemini output")
        return LLMOutput(
            sql_query="",
            chart_type="table",
            error=f"Invalid LLM output: {exc}",
        )

    logger.info("Gemini SQL generation completed")
    return llm_output
