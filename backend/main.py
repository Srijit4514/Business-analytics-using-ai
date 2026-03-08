import logging

from fastapi import FastAPI, HTTPException

from config import LOG_LEVEL
from database import initialize_database
from models import QueryRequest, QueryResponse
from query_service import process_natural_language_query

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Conversational AI BI Backend", version="1.0.0")


@app.on_event("startup")
def startup_event() -> None:
    try:
        initialize_database()
    except Exception as exc:
        logger.exception("Failed during startup initialization")
        raise RuntimeError(f"Database initialization failed: {exc}") from exc


@app.post("/query", response_model=QueryResponse)
def query_endpoint(payload: QueryRequest) -> QueryResponse:
    try:
        return process_natural_language_query(payload.question)
    except Exception as exc:
        logger.exception("Unexpected error in /query")
        raise HTTPException(status_code=500, detail=f"Unexpected backend error: {exc}") from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
