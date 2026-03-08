# Conversational AI for Instant Business Intelligence Dashboards (Backend)

## Project Structure

```text
project_root/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── llm_service.py
│   ├── query_service.py
│   ├── schema_loader.py
│   ├── models.py
│   ├── utils.py
│   └── requirements.txt
└── data/
    └── sales.csv
```

## Setup

1. Create and activate environment (already created as `.venv`):

```bash
cd backend
../.venv/bin/pip install -r requirements.txt
```

2. Configure Gemini API key in `backend/config.py`:

```python
API_KEY = ""
```

Keep it blank until you add your own key.

## Run Backend

```bash
cd backend
../.venv/bin/uvicorn main:app --reload
```

## Main Endpoint

### `POST /query`

Request:

```json
{
  "question": "Show revenue by region"
}
```

Example response:

```json
{
  "sql_query": "SELECT region, SUM(revenue) AS total_revenue FROM sales GROUP BY region ORDER BY total_revenue DESC",
  "chart_type": "bar_chart",
  "data": [
    {"region": "South", "total_revenue": 2900.2},
    {"region": "North", "total_revenue": 1510.49},
    {"region": "West", "total_revenue": 1125.9},
    {"region": "East", "total_revenue": 1290.65}
  ],
  "x_axis": "region",
  "y_axis": "total_revenue",
  "description": "Revenue aggregated by region",
  "error": null
}
```

## Backend Pipeline

1. Accept natural language query via FastAPI
2. Extract live DB schema from SQLite
3. Send schema + question to Gemini
4. Parse and validate LLM SQL output
5. Execute SQL on SQLite
6. Return structured JSON response
