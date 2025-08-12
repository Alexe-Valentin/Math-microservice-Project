# src/models.py

from datetime import datetime
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from .database import db
from flask_sqlalchemy.model import Model  # type: ignore
from typing import Any


class RequestLog(db.Model, Model):  # type: ignore
    """
    Model to persist all API math requests and their results.
    """

    __tablename__ = "request_logs"

    id: Any = db.Column(db.Integer, primary_key=True)
    endpoint: Any = db.Column(db.String(50), nullable=False)
    input_value: Any = db.Column(db.String(100), nullable=False)
    result: Any = db.Column(db.String(100), nullable=False)
    timestamp: Any = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f"<RequestLog {self.endpoint}({self.input_value}) = "
            f"{self.result} @ {self.timestamp}>"
        )


class User(db.Model, Model):  # type: ignore
    """
    User model for authentication and JWT login.
    Stores username and securely-hashed password.
    """

    __tablename__ = "users"

    id: Any = db.Column(db.Integer, primary_key=True)
    username: Any = db.Column(db.String(80), unique=True, nullable=False)
    password_hash: Any = db.Column(db.String(128), nullable=False)
    created_at: Any = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        """
        Hash and store the user's password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check a plain password against the stored hash.
        """
        return check_password_hash(self.password_hash, password)
