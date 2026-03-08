import logging
import sqlite3
from contextlib import contextmanager
from typing import Any, Generator

import pandas as pd

from config import CSV_PATH, DB_PATH, MAX_ROWS

logger = logging.getLogger(__name__)


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def initialize_database() -> None:
    logger.info("Initializing SQLite database at %s", DB_PATH)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    dataframe = pd.read_csv(CSV_PATH)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER,
                date TEXT,
                region TEXT,
                product TEXT,
                category TEXT,
                revenue FLOAT,
                quantity INTEGER
            )
            """
        )
        cursor.execute("DELETE FROM sales")
        conn.commit()

        dataframe.to_sql("sales", conn, if_exists="append", index=False)
        conn.commit()

    logger.info("Database initialized with %s rows from %s", len(dataframe), CSV_PATH)


def execute_select_query(sql_query: str) -> list[dict[str, Any]]:
    logger.info("Executing SQL query")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchmany(MAX_ROWS)
        result = [dict(row) for row in rows]

    logger.info("SQL execution completed with %s rows", len(result))
    return result
