# Math Microservice – Flask, JWT, Pydantic, Swagger

A production-ready microservice for math operations, built in Flask with RESTful APIs, JWT authentication, Pydantic validation, Prometheus monitoring, Redis/Kafka integration, and Swagger UI for interactive documentation.

---

## Features

- **Endpoints:** Power, Fibonacci, Factorial (`/api/math/...`)
- **Authentication:** JWT login at `/auth/login`
- **Validation:** Input validation & output serialization with Pydantic
- **Persistence:** SQLite via SQLAlchemy
- **Caching:** Redis (optional)
- **Streaming/Logging:** Kafka (optional)
- **Docs:** Swagger UI at `/apidocs`
- **Monitoring:** Prometheus metrics at `/metrics`
- **Code Quality:** Auto-formatting, linting, type-checking

---

## Quickstart

### 1. Clone & Install Dependencies

```bash
python -m venv .venv
# Activate your venv (Windows)
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Create the Database

```bash
python -m src.create_tables
```

### 3. Seed a User

```bash
python -m src.cli create-user alice
# Enter and confirm password when prompted
```

### 4. Run the Application

```bash
python -m src.app
```
- **Swagger UI:** [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)
---

## Usage

### Login and Get a JWT Token

**POST** to `/auth/login` :

```json
{
  "username": "alice",
  "password": "alice"
}
```

Response:

```json
{ "access_token": "..." }
```

### Test Endpoints (with JWT)

All `/api/math/...` endpoints require the `Authorization: Bearer <token>` header.

- **Power**: `/api/math/pow?base=2&exp=8` → `{ "result": 256 }`
- **Fibonacci**: `/api/math/fib?n=10` → `{ "result": 55 }`
- **Factorial**: `/api/math/factorial?n=5` → `{ "result": 120 }`

You can test these in Swagger UI after clicking “Authorize” and pasting your JWT token (`Bearer ...`).

---

## Validation

- Missing or invalid input (e.g. `n=foo` or missing `base`) returns **400 Bad Request** with a helpful message.
- Authentication errors return **401 Unauthorized**.

---

## Development & Testing

- **Lint:** `flake8 src/ tests/`
- **Format:** `black src/ tests/`
- **Type-check:** `mypy src/`
- **Test:** `pytest -q`

---

## Docker Support (when ready)

### Build

```bash
docker build -t math-microservice .
```

### Run

```bash
docker run -p 5000:5000 math-microservice
```

(Optional) Add Redis/Kafka via Docker Compose.

---

## Project Structure


PythonProject/
├─ src/
│  ├─ __init__.py
│  ├─ app.py
│  ├─ cli.py
│  ├─ config.py
│  ├─ create_tables.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ services.py
│  ├─ controllers/
│  │  ├─ __init__.py
│  │  ├─ auth_controller.py      # Handles /auth/login (JWT authentication)
│  │  └─ math_controller.py      # Handles /api/math/{pow,fib,factorial}
│  └─ utils/
│     ├─ __init__.py
│     ├─ cache.py                 # Redis cache integration
│     └─ kafka_logger.py          # Kafka logging integration
│
├─ instance/
│  └─ requests.db                 # SQLite database file (created at runtime)
│
├─ tests/
│  ├─ __init__.py
│  ├─ conftest.py                  # Pytest fixtures (auto JWT, test client)
│  └─ test_math_api.py             # Tests for math endpoints
│
├─ .flake8
├─ mypy.ini
├─ README.md
└─ requirements.txt


---

## API Docs

- Visit [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)
- Click “Authorize” (lock icon) and paste `Bearer <token>`
- Try endpoints interactively!

---

## Notes

- Redis and Kafka are optional; the app will gracefully degrade if not present.
- All validation and serialization is handled by Pydantic for safety and maintainability.
- You can extend the service with new endpoints and models easily!
