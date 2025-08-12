import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask secret
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "instance", "requests.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Redis (caching)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    # Kafka (logging/streaming)
    KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
    KAFKA_CLIENT_ID = os.getenv("KAFKA_CLIENT_ID", "math-service")
    # Login
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-change-me")
    JWT_ACCESS_TOKEN_EXPIRES = False  # or set a timedelta
