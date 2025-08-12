# Math Microservice – Flask, JWT, Pydantic, Swagger

This is a production-ready microservice for math operations, built in Flask with RESTful APIs, JWT authentication, Pydantic validation, Prometheus monitoring, Redis/Kafka integration, and Swagger UI for documentation/testing.

---

## Features

- **Power, Fibonacci, Factorial** endpoints (`/api/math/...`)
- **JWT login** at `/auth/login`
- **Input validation** and output serialization with Pydantic
- **SQLite persistence** (via SQLAlchemy)
- **Redis** (optional, for caching)
- **Kafka** (optional, for logging/streaming)
- **Swagger UI** (`/apidocs`) for interactive documentation & live testing
- **Prometheus metrics** at `/metrics`
- **Modern codebase:** auto-formatting, linting, type-checking

---

## Quickstart

### 1. **Clone and Install Dependencies**

```bash
python -m venv .venv
# Activate your venv (on Windows)
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
2. Create the Database
bash
Copy
Edit
python -m src.create_tables
3. Seed a User
bash
Copy
Edit
python -m src.cli create-user alice
# Enter and confirm password when prompted
4. Run the Application
bash
Copy
Edit
python -m src.app
Your API runs at: http://127.0.0.1:5000

Swagger UI: http://127.0.0.1:5000/apidocs

Prometheus: http://127.0.0.1:5000/metrics

Usage
Login and Get a JWT Token
POST to /auth/login (Swagger UI or any HTTP client):

json
Copy
Edit
{
  "username": "alice",
  "password": "alice"
}
Response: { "access_token": "..." }

Test Endpoints (with JWT)
All /api/math/... endpoints require the Authorization: Bearer <token> header.

Power: /api/math/pow?base=2&exp=8 → { "result": 256 }

Fibonacci: /api/math/fib?n=10 → { "result": 55 }

Factorial: /api/math/factorial?n=5 → { "result": 120 }

You can test these in Swagger UI after clicking “Authorize” and pasting your JWT token (Bearer ...).

Validation
Missing or invalid input (e.g. n=foo or base=) returns 400 Bad Request with a helpful message.

Authentication errors return 401 Unauthorized.

Development & Testing
Lint: flake8 src/ tests/

Format: black src/ tests/

Type-check: mypy src/

Test: pytest -q

Docker Support (when ready)
Build:

bash
Copy
Edit
docker build -t math-microservice .
Run:

bash
Copy
Edit
docker run -p 5000:5000 math-microservice
(Optional) Add Redis/Kafka via Docker Compose.

Project Structure
pgsql
Copy
Edit
PythonProject/
├─ src/
│   ├─ app.py
│   ├─ cli.py
│   ├─ config.py
│   ├─ create_tables.py
│   ├─ controllers/
│   ├─ database.py
│   ├─ models.py
│   ├─ schemas.py
│   └─ services.py
├─ instance/
│   └─ requests.db
├─ requirements.txt
└─ tests/
API Docs
Visit http://127.0.0.1:5000/apidocs

Click “Authorize” (lock icon) and paste Bearer <token>

Try endpoints interactively!

Notes
Redis and Kafka are optional; the app will gracefully degrade if not present.

All validation and serialization is now handled by Pydantic for safety and maintainability.

You can extend the service with new endpoints and models easily!

