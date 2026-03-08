import logging

from database import execute_select_query
from llm_service import generate_sql_with_gemini
from models import QueryResponse
from schema_loader import extract_database_schema
from utils import validate_sql_query

logger = logging.getLogger(__name__)


def process_natural_language_query(question: str) -> QueryResponse:
    logger.info("Received user question: %s", question)

    schema_text = extract_database_schema()
    llm_output = generate_sql_with_gemini(question, schema_text)

    if llm_output.error:
        logger.error("LLM error: %s", llm_output.error)
        return QueryResponse(
            sql_query=llm_output.sql_query,
            chart_type=llm_output.chart_type,
            data=[],
            x_axis=llm_output.x_axis,
            y_axis=llm_output.y_axis,
            description=llm_output.description,
            error=llm_output.error,
        )

    is_valid, validation_error = validate_sql_query(llm_output.sql_query)
    if not is_valid:
        logger.error("SQL validation failed: %s", validation_error)
        return QueryResponse(
            sql_query=llm_output.sql_query,
            chart_type="table",
            data=[],
            x_axis=llm_output.x_axis,
            y_axis=llm_output.y_axis,
            description=llm_output.description,
            error=f"SQL validation failed: {validation_error}",
        )

    try:
        query_result = execute_select_query(llm_output.sql_query)
    except Exception as exc:
        logger.exception("SQL execution failed")
        return QueryResponse(
            sql_query=llm_output.sql_query,
            chart_type=llm_output.chart_type,
            data=[],
            x_axis=llm_output.x_axis,
            y_axis=llm_output.y_axis,
            description=llm_output.description,
            error=f"Database query failed: {exc}",
        )

    return QueryResponse(
        sql_query=llm_output.sql_query,
        chart_type=llm_output.chart_type,
        data=query_result,
        x_axis=llm_output.x_axis,
        y_axis=llm_output.y_axis,
        description=llm_output.description,
        error=None,
    )
