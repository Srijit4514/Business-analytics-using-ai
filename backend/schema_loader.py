import logging

from database import get_connection

logger = logging.getLogger(__name__)


def extract_database_schema() -> str:
    logger.info("Extracting database schema")

    lines: list[str] = []
    with get_connection() as conn:
        cursor = conn.cursor()
        tables = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()

        for table in tables:
            table_name = table[0]
            lines.append(f"Table: {table_name}")
            columns = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
            for column in columns:
                lines.append(f"- {column[1]} ({column[2]})")
            lines.append("")

    schema_text = "\n".join(lines).strip()
    logger.info("Schema extraction completed")
    return schema_text
