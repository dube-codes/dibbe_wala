# Dibbe Wala

Dibbe Wala is a small FastAPI service for creating and listing delivery orders, and viewing daily order counts by status. Orders are stored in a local SQLite database.

## Features

- Create delivery orders with a customer name, delivery address, and items.
- Assign new orders the `preparing` status by default.
- List orders with optional status filtering and pagination.
- View daily order totals grouped by status.
- Create database tables automatically when the application starts.

## Tech stack

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn

## Project structure

```text
.
├── main.py             # FastAPI app and router setup
├── database.py         # SQLite engine, session, and table setup
├── models.py           # Order model, status enum, and data schemas
├── routes/
│   ├── orders.py       # Order creation and listing endpoints
│   └── stats.py        # Daily order statistics endpoint
├── requirements.txt
└── README.md
```

## Installation and setup

Create and activate a virtual environment, then install the project dependencies:

```bash
python -m venv .venv
```

On Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The application uses SQLite at `sqlite:///dabbewala.db`. It creates the database tables on startup; no separate database service or migration command is configured.

## Run the project

From the project directory, start the development server:

```bash
uvicorn main:app --reload
```

The root endpoint is available at `http://127.0.0.1:8000/`.

## API endpoints

All order and statistics routes use the `/api/v1` prefix.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Welcome message with the API version |
| `POST` | `/api/v1/orders/` | Create an order |
| `GET` | `/api/v1/orders/` | List orders |
| `GET` | `/api/v1/stats/daily` | Get order counts for a date, grouped by status |

### Create an order

`POST /api/v1/orders/`

Request:

```json
{
  "customer_name": "Asha Sharma",
  "delivery_address": "12 Market Road",
  "items": "Lunch box, lemonade"
}
```

The response contains the created order, including its generated `id`, default `status`, and timestamps:

```json
{
  "id": 1,
  "customer_name": "Asha Sharma",
  "delivery_address": "12 Market Road",
  "items": "Lunch box, lemonade",
  "status": "preparing",
  "created_at": "2026-11-09T12:00:00+00:00",
  "updated_at": "2026-11-09T12:00:00+00:00"
}
```

### List orders

`GET /api/v1/orders/`

Optional query parameters:

| Parameter | Description |
|---|---|
| `status` | Filter by `preparing`, `picked_up`, `in_transit`, `delivered`, or `cancelled` |
| `created_date` | Intended to filter by creation date in `YYYY-MM-DD` format; see Known limitations |
| `skip` | Number of orders to skip; defaults to `0` |
| `limit` | Maximum orders to return; defaults to `10`, with a maximum of `100` |

Example:

```text
GET /api/v1/orders/?status=preparing&skip=0&limit=10
```

The response is a JSON array of order objects using the same fields as the create-order response.

### Get daily statistics

`GET /api/v1/stats/daily`

The optional `stats_date` query parameter accepts a date in `YYYY-MM-DD` format. If omitted, the API uses the current date.

Example:

```text
GET /api/v1/stats/daily?stats_date=2026-11-09
```

Example response:

```json
{
  "date": "2026-11-09",
  "total_orders": 3,
  "by_status": {
    "preparing": 1,
    "picked_up": 1,
    "in_transit": 0,
    "delivered": 1,
    "cancelled": 0
  }
}
```

## API documentation

With the server running, FastAPI's Swagger UI is available at `http://127.0.0.1:8000/docs`. The OpenAPI schema is at `http://127.0.0.1:8000/openapi.json`, and ReDoc is at `http://127.0.0.1:8000/redoc`.

## Environment variables

No environment variables are read by the application. The SQLite database URL is currently set directly in `database.py`.

## Known limitations

- The order-list `created_date` parameter is a string passed to `datetime.combine`, which expects a date value. Supplying this parameter can cause the request to fail.
- There is no order-update endpoint. An `OrderUpdate` schema exists, but it is not used by a route.

## Potential improvements

- Parse and validate `created_date` so the order-list date filter works as intended.
- Add an order-update endpoint using the existing `OrderUpdate` schema.
- Add automated tests and database migrations as the project grows.
- Make the SQLite database URL configurable instead of hard-coding it.
