import pytest
import logging
from src.app import create_app
from flask_jwt_extended import create_access_token

# --- Professional Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
test_logger = logging.getLogger("math-microservice.test")


# --- Pytest Fixture with Automatic JWT ---
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            token = create_access_token(identity="testuser")
        client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        test_logger.info("Test client initialized with JWT token for 'testuser'.")
        yield client


# --- Tests with Logging ---
def test_pow_success(client):
    test_logger.info("Testing endpoint: /api/math/pow?base=2&exp=8")
    rv = client.get("/api/math/pow?base=2&exp=8")
    assert (
        rv.status_code == 200
    ), f"Expected 200, got {rv.status_code} (body: {rv.data})"
    assert rv.get_json() == {"result": 256}
    test_logger.info("✅ Power endpoint returned correct result (2^8 = 256)")


def test_fib_success(client):
    test_logger.info("Testing endpoint: /api/math/fib?n=7")
    rv = client.get("/api/math/fib?n=7")
    assert (
        rv.status_code == 200
    ), f"Expected 200, got {rv.status_code} (body: {rv.data})"
    assert rv.get_json() == {"result": 13}
    test_logger.info("✅ Fibonacci endpoint returned correct result (fib(7) = 13)")


def test_fact_success(client):
    test_logger.info("Testing endpoint: /api/math/factorial?n=6")
    rv = client.get("/api/math/factorial?n=6")
    assert (
        rv.status_code == 200
    ), f"Expected 200, got {rv.status_code} (body: {rv.data})"
    assert rv.get_json() == {"result": 720}
    test_logger.info("✅ Factorial endpoint returned correct result (6! = 720)")
